from flask import redirect, render_template, request, url_for
from app.extensions import limiter
from . import fileIO


@fileIO.route('/upload', methods=['GET', 'POST'])
def upload_snippet():
    if request.method == 'POST':
        # Handle the file and form data here
        # If user not logged in, redirect to failure
        # If successful, redirect to success
        return redirect(url_for('fileIO.success'))
    return render_template('upload.html')

@fileIO.route('/new-tag', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'POST':
        # Process new tag request
        return redirect(url_for('fileIO.success'))
    return render_template('new-tag.html')

@fileIO.route('/new-language', methods=['GET', 'POST'])
def new_language():
    if request.method == 'POST':
        # Process new language request
        return redirect(url_for('fileIO.success'))
    return render_template('new-language.html')

@fileIO.route('/success')
def success():
    return render_template('success.html')

@fileIO.route('/failure')
def failure():
    return render_template('failure.html')




