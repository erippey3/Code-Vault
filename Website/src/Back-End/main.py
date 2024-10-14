from flask import Flask, redirect, render_template, Response, abort, request, send_from_directory, Request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import safe_join
import logging
from logging.handlers import RotatingFileHandler

import os


app = Flask(__name__, template_folder='./')
limiter = Limiter(get_remote_address, app=app, default_limits=["600 per day", "300 per hour"])
handler = RotatingFileHandler('file_browser.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


repository_dir = os.environ.get('REPO_DIR')
UPLOAD_FOLDER = os.path.abspath(repository_dir)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {
    'txt',   # Text files
    'pdf',   # PDF files
    'png',   # Image file
    'jpg', 'jpeg',  # Image files
    'gif',   # Image files
    'md',    # Markdown files
    'c',     # C source code
    'cpp',   # C++ source code
    'h',     # C/C++ headers
    'hpp',   # C++ headers
    'py',    # Python files
    'java',  # Java files
    'js',    # JavaScript files
    'html',  # HTML files
    'css',   # CSS files
    'yaml',  # YAML files
    'yml',   # YAML alternate extension
    'json',  # JSON files
    'xml',   # XML files
    'toml',  # TOML config files
    'ini',   # INI config files
    'sh',    # Shell script files
    'bash',  # Bash script files
    'go',    # Go files
    'rs',    # Rust files
    'ts',    # TypeScript files
    'php',   # PHP files
    'rb',    # Ruby files
    'r',     # R language files
    'swift', # Swift files
    'kt',    # Kotlin files
    'pl',    # Perl files
    'ps1',   # PowerShell scripts
    'sql',   # SQL scripts
    'cs',    # C# files
    'dart',  # Dart files
    'scss',  # SASS/SCSS files
    'less',  # LESS files
    'log',   # Log files
    'bat',   # Batch files
    'rs',    # Rust files
    'env',   # Environment files
    'dockerfile',  # Dockerfile
    'makefile',  # Makefile
}


@app.errorhandler(403)
def forbidden(e):
    app.logger.warning(f"403 Access Denied: {e}")
    return "Access denied", 403


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
@app.route('/<path:subpath>')
@limiter.limit("100 per minute")
def file_browser(subpath=''):
    full_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, subpath))
    
    if not full_path.startswith(os.path.abspath(UPLOAD_FOLDER)):
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
