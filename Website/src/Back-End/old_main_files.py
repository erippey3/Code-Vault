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
    return send_from_directory(root_dir, filepath, as_attachment=True)

@app.route('/downloads')
def downloads():
    root_dir = os.path.abspath('your/root/directory')
    files = []
    for filename in os.listdir(root_dir):
        full_path = os.path.join(root_dir, filename)
        if os.path.isfile(full_path):
            files.append(filename)
    return render_template('downloads.html', files=files)




@app.route('/upload', methods=['GET', 'POST'])
def upload(filepath):
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            abort(400)  # Bad Request

        file = request.files['file']

        # If the user does not select a file
        if file.filename == '':
            abort(400)  # Bad Request

        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the file
        file.save(full_path)

        return redirect(url_for('uploaded_file', filename=filename))

    # If GET request, render the upload form
    return render_template('upload.html')