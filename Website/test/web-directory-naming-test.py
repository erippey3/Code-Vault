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




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


print(allowed_file('file.c'))