from flask import render_template, request, send_from_directory, abort, current_app
import os
from app.extensions import limiter
from . import main



@main.route('/favicon.ico')
def favicon():
    return send_from_directory('vault.ico', mimetype='image/vnd.microsoft.icon')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
@main.route('/<path:subpath>')
@limiter.limit("40 per minute")
def file_browser(subpath=''):
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
    

@main.route('/search')
def search_projects():
    query_param = request.args.get('q', '')
    tags = request.args.getlist('tags')  # multiple checkbox values

    # TODO: Implement Elasticsearch query here
    # For now, let's fake it:
    projects = []  # This would be a list of dicts from Elasticsearch hits
    # Example:
    # projects = [
    #    {"id": 1, "name": "Project Alpha", "language": "Python", "tags": ["GUI", "DATA STRUCTURES"]},
    #    {"id": 2, "name": "Project Beta", "language": "Java", "tags": ["FILE PARSING"]}
    # ]

    return render_template('search_results.html', projects=projects)


