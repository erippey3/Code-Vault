from flask import request, redirect, url_for, flash, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask_dance.contrib.github import github
from app.model import User
from app import db
from  . import auth
from app.extensions import limiter


@auth.route('/login')
@limiter.limit("5 per minute")
def login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            github_id = str(account_info_json['id'])
            username = account_info_json['login']

            # Fetch primary email if email is not public
            email = account_info_json.get('email')
            if not email:
                emails = github.get('/user/emails')
                if emails.ok:
                    emails_json = emails.json()
                    # Find primary email
                    for e in emails_json:
                        if e.get('primary') and e.get('verified'):
                            email = e.get('email')
                            break

            if not email:
                flash('No email address associated with your GitHub account')
                return redirect(url_for('main.file_browser'))
            
            if not email.endswith('@vt.edu'):
                flash('You must have an email associated with Virginia Tech to use this application')
                return redirect(url_for('main.file_browser'))

            # Check if user exists
            user = User.query.filter_by(github_id=github_id).first()
            if not user:
                # Create new user
                user = User(username=username, email=email, github_id=github_id, verified=True)
                db.session.add(user)
                db.session.commit()

            # Log the user in
            session['username'] = user.username
            flash('Logged in successfully.')
            return redirect(url_for('main.file_browser'))

        flash('Failed to fetch user info from GitHub.')
        return redirect(url_for('main.file_browser'))



@auth.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

