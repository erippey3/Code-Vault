import os
import uuid
from flask import current_app, flash, redirect, render_template, request, url_for
from app.extensions import limiter
from . import fileIO
from app.extensions import db, es
from app.model import Project, Tag, ProjectTag, User
from flask_login import current_user, login_required


@fileIO.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_snippet():
    if request.method == 'POST':
        snippet_name = request.form.get('snippet_name', None)
        language = request.form.get('language', None)
        tags = request.form.getlist('tags')
        print(f'tags {tags}')

        if not snippet_name or not language:
            flash("Snippet name and language are required.")
            return redirect(url_for('fileIO.upload_snippet'))
    
        zip_file = request.files.get('file')  # This is the zipped project
        if not zip_file:
            flash("No file uploaded")
            return redirect(url_for('fileIO.upload_snippet'))
        
        target_tag = tags[0] if tags else ''
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], language, target_tag)
        os.makedirs(upload_path, exist_ok=True)

        project_folder = snippet_name
        project_full_path = os.path.join(upload_path, project_folder)
        os.makedirs(project_full_path, exist_ok=True)

        zip_path = os.path.join(project_full_path, "project.zip")
        zip_file.save(zip_path)

        import zipfile
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(project_full_path)
            # If successful, delete the zip
            os.remove(zip_path)
        except Exception as e:
            # Handle errors: cleanup, log, etc.
            flash(f"Error extracting zip: {e}")
            return redirect(url_for('fileIO.upload_snippet'))


        # postgres create project
        new_project = Project(
            name=snippet_name,
            path=project_full_path,
            language = language,
            uploader_id = current_user.id,
            is_public=True
        )

        db.session.add(new_project)
        db.session.flush()

        for tag in tags:
            tag_obj = Tag.query.filter_by(tag_name=tag).first()
            if not tag_obj:
                tag_obj = Tag(tag_name=tag)
                db.session.add(tag_obj)
                db.session.flush()
            new_project.tags.append(tag_obj)
        db.session.commit()

        # elastic search upload
        doc = {
            'id': new_project.id,
            'name' : new_project.name,
            'path' : new_project.path,
            'language' : new_project.language,
            'tags' : [t.tag_name for t in new_project.tags],
            'is_public' : new_project.is_public,
            'uploader_id' : current_user.id, 
            'username' : current_user.username
        }

        es.index(index='projects_index', id=new_project.id, document=doc)

        flash('project uploaded successfully!')
        return redirect(url_for('main.file_browser', subpath='/'.join(filter(None, [language, target_tag, snippet_name]))))


    return render_template('upload.html')



@fileIO.route('/new-tag', methods=['GET', 'POST'])
@login_required
def new_tag():
    if request.method == 'POST':
        # Process new tag request
        return redirect(url_for('fileIO.success'))
    return render_template('new-tag.html')



@fileIO.route('/new-language', methods=['GET', 'POST'])
@login_required
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




