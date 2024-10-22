from flask import render_template, send_from_directory, abort, current_app
import os
from app.extensions import limiter
from . import main



@main.route('/favicon.ico')
def favicon():
    return send_from_directory(main.template_folder,
                               'vault.ico', mimetype='image/vnd.microsoft.icon')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
@main.route('/<path:subpath>')
@limiter.limit("40 per minute")
def file_browser(subpath=''):
    print(current_app.template_folder)
    full_path = os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER'], subpath))
    
    if not full_path.startswith(os.path.abspath(current_app.config['UPLOAD_FOLDER'])):
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