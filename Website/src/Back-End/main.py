from flask import Flask, redirect, render_template, Response, abort, request, send_from_directory, Request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import safe_join
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime
from app import create_app
from model import db

import os


app = create_app()
limiter = Limiter(get_remote_address, app=app, default_limits=["600 per day", "300 per hour"])

with app.app_context():
    db.create_all()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.template_folder,
                               'vault.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(403)
def forbidden(e):
    app.logger.warning(f"403 Access Denied: {e}")
    return "Access denied", 403


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
@app.route('/<path:subpath>')
@limiter.limit("100 per minute")
def file_browser(subpath=''):
    full_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], subpath))
    
    if not full_path.startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
        return "Access denied", 403
    
    if os.path.isdir(full_path):
        dirs = sorted([d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))])
        files = sorted([f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f)) and allowed_file(f)])
        
        parent_path = os.path.dirname(subpath) if subpath else None
        
        return render_template('file_browser.html', dirs=dirs, files=files, current_path=subpath, parent_path=parent_path)

    else:
        if not allowed_file(os.path.basename(subpath)):
            return "File type not allowed", 403
        return send_from_directory(os.path.dirname(full_path), os.path.basename(subpath))







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
