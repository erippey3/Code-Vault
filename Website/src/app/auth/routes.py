import secrets
from urllib.parse import urlencode
from flask import abort, redirect, request, url_for, flash, session, current_app
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_dance.contrib.github import github
import requests
from app.model import User
from app import db
from  . import auth
from app.extensions import limiter


@auth.route('/login/<provider>')
@limiter.limit("5 per minute")
def login(provider):
    if session.get('user_id'):
        return redirect(url_for('main.file_browser'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    
    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('auth.login_callback', 
                                provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    return redirect(provider_data['authorize_url'] + '?' + qs)



@auth.route('/login/callback/<provider>')
@limiter.limit("5 per minute")
def login_callback(provider):
    if session.get('user_id'):
        return redirect(url_for('main.file_browser'))
    
    current_app.logger.debug(f"Session oauth2_state: {session.get('oauth2_state')}")
    current_app.logger.debug(f"Request state: {request.args.get('state')}")

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('main.file_browser'))

    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # Exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('auth.login_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)

    access_token = response.json().get('access_token')
    if not access_token:
        abort(401)

    # Fetch the user's email address
    email_response = requests.get(provider_data['userinfo']['email_url'], headers={
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    })
    if email_response.status_code != 200:
        abort(401)

    emails = email_response.json()
    # Find the primary email
    email = next((e['email'] for e in emails if e.get('primary') and e.get('verified')), None)

    if not email:
        flash('No verified primary email address associated with your GitHub account')
        return redirect(url_for('main.file_browser'))

    if not email.endswith('@vt.edu'):
        flash('You must have an email associated with Virginia Tech to use this application')
        return redirect(url_for('main.file_browser'))

    # Fetch the user's GitHub ID and username
    profile_response = requests.get(provider_data['userinfo']['profile_url'], headers={
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    })
    if profile_response.status_code != 200:
        abort(401)

    profile_data = profile_response.json()
    github_id = str(profile_data.get('id'))
    username = profile_data.get('login')

    if not github_id or not username:
        flash('Unable to retrieve your GitHub profile information')
        return redirect(url_for('main.file_browser'))

    # Check if the user exists in the database
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        # Create a new user
        user = User(username=username, email=email, github_id=github_id)
        db.session.add(user)
        db.session.commit()

    # Log the user in
    session['user_id'] = user.id
    session['username'] = user.username
    print (session.get('username'))
    flash('Logged in successfully.')
    return redirect(url_for('main.file_browser'))


# @auth.route('/login/<provider>')
# @limiter.limit("5 per minute")
# def login():
#     if not github.authorized:
#         return redirect(url_for('github.login'))
#     else:
#         account_info = github.get('/user')
#         if account_info.ok:
#             account_info_json = account_info.json()
#             github_id = str(account_info_json['id'])
#             username = account_info_json['login']

#             # Fetch primary email if email is not public
#             email = account_info_json.get('email')
#             if not email:
#                 emails = github.get('/user/emails')
#                 if emails.ok:
#                     emails_json = emails.json()
#                     # Find primary email
#                     for e in emails_json:
#                         if e.get('primary') and e.get('verified'):
#                             email = e.get('email')
#                             break

#             if not email:
#                 flash('No email address associated with your GitHub account')
#                 return redirect(url_for('main.file_browser'))
            
#             if not email.endswith('@vt.edu'):
#                 flash('You must have an email associated with Virginia Tech to use this application')
#                 return redirect(url_for('main.file_browser'))

#             # Check if user exists
#             user = User.query.filter_by(github_id=github_id).first()
#             if not user:
#                 # Create new user
#                 user = User(username=username, email=email, github_id=github_id, verified=True)
#                 db.session.add(user)
#                 db.session.commit()

#             # Log the user in
#             session['username'] = user.username
#             flash('Logged in successfully.')
#             return redirect(url_for('main.file_browser'))

#         flash('Failed to fetch user info from GitHub.')
#         return redirect(url_for('main.file_browser'))


@auth.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

