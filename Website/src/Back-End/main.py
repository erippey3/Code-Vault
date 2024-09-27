from flask import Flask, render_template, Response, abort, request, send_from_directory, Request
from werkzeug.utils import safe_join

import os

app = Flask(__name__, template_folder='../Front-End')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download/<path:filepath>')
def download(filepath):
    # Define the root directory for file storage
    root_dir = os.path.abspath('your/root/directory')

    # Securely join the root directory and the requested file path
    try:
        full_path = safe_join(root_dir, filepath)
    except ValueError:
        # Invalid path; potential directory traversal attack
        abort(403)  # Forbidden

    # Check if the file exists
    if not os.path.isfile(full_path):
        abort(404)  # Not Found

    # Serve the file
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/upload/<path:filepath>', methods=['POST'])
def upload(filepath):
    # Define the root directory for file storage
    root_dir = os.path.abspath('your/root/directory')

    # Securely join the root directory and the requested file path
    try:
        full_path = safe_join(root_dir, filepath)
    except ValueError:
        # Invalid path; potential directory traversal attack
        abort(403)  # Forbidden

    # Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Save the uploaded file
    with open(full_path, 'wb') as f:
        for chunk in iter(lambda: request.stream.read(4096), b''):
            f.write(chunk)

    return 'Upload complete', 201  # Created



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
