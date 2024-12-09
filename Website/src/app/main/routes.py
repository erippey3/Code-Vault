from flask import render_template, request, send_from_directory, abort, current_app
import os
from app.extensions import limiter, db, es
from app.model import Project, Tag
from . import main



@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(main.root_path, 'templates'),
        'vault.ico',
        mimetype='image/vnd.microsoft.icon'
    )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
@main.route('/<path:subpath>')
@limiter.limit("40 per minute")
def file_browser(subpath=''):
    full_path = os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER'], subpath))
    
    if not full_path.startswith(os.path.abspath(current_app.config['UPLOAD_FOLDER'])):
        return "Access denied", 403
    
    project_path = in_project(full_path)
    
    if os.path.isdir(full_path):
        dirs = sorted([d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))])
        files = sorted([f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f)) and allowed_file(f)])
        
        parent_path = os.path.dirname(subpath) if subpath else None
        
        return render_template('file_browser.html', dirs=dirs, files=files, current_path=subpath, parent_path=parent_path, project_path=project_path)

    else:
        if not allowed_file(os.path.basename(subpath)):
            return "File type not allowed", 403
        return send_from_directory(os.path.dirname(full_path), os.path.basename(subpath))
    


@main.route('/search', methods=['GET'])
@limiter.limit("10 per minute")
def search_projects():
    # Get query params
    query_param = request.args.get('q', '').strip()
    tags = request.args.getlist('tags')  # Multiple selected tags

    # Initialize the results list
    projects = []

    # Step 1: Full-text search with Elasticsearch
    if query_param:
        es_query = {
            "query": {
                "multi_match": {
                    "query": query_param,
                    "fields": ["name^2", "description", "language"]
                }
            }
        }
        es_results = es.search(index="projects_index", body=es_query)
        es_ids = [hit["_source"]["id"] for hit in es_results["hits"]["hits"]]

        # Fetch matching projects from PostgreSQL
        if es_ids:
            projects = db.session.query(Project).filter(Project.id.in_(es_ids)).all()

    # Step 2: Filter by tags if provided
    if tags:
        projects = (
            db.session.query(Project)
            .join(Project.tags)  # Assuming Project and Tag are related via SQLAlchemy
            .filter(Tag.tag_name.in_(tags))
            .all()
        )

    # Serialize the projects for rendering
    serialized_projects = [
        {
            "id": project.id,
            "name": project.name,
            "language": project.language,
            "tags": [tag.tag_name for tag in project.tags],
            "path": os.path.relpath(project.path, current_app.config['UPLOAD_FOLDER'])  # Relative path for file_browser
        }
        for project in projects
    ]

    return render_template('search_results.html', projects=serialized_projects)


def in_project(full_path):
    """
    Checks if the current directory belongs to a project in the database.
    Returns the project path if found, else None.
    """
    while full_path.startswith(os.path.abspath(current_app.config['UPLOAD_FOLDER'])):
        # Check if the directory is associated with a project
        project = Project.query.filter_by(path=full_path).first()
        if project:
            return os.path.relpath(project.path, current_app.config['UPLOAD_FOLDER'])  # Return the project path
        full_path = os.path.dirname(full_path)  # Move up one directory level

    return None  # No project found