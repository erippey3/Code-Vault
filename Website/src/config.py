import os
from dotenv import load_dotenv
import redis
from datetime import timedelta

# Load environment variables from the .env file
load_dotenv()

class Config:

    # general server info
    SERVER_NAME= os.getenv('SERVER_NAME', '192.168.44.4:54003')
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', 'http')
    OATHLIB_INSECURE_TRANSPORT = os.getenv('OATHLIB_INSECURE_TRANSPORT', '0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'here_is_the_key_for_our_project')  
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('REPO_DIR'))

    # database management
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    #session settings
    SESSION_TYPE= 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.from_url('redis://redis:6379/0')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE= None
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)


    OAUTH2_PROVIDERS = {
        'github': {
            'client_id': os.environ.get('GITHUB_CLIENT_ID'),
            'client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'token_url': 'https://github.com/login/oauth/access_token',
            'userinfo': {
                'email_url': 'https://api.github.com/user/emails',
                'profile_url': 'https://api.github.com/user',
            },
            'scopes': ['user:email', 'read:user'],
        },
        # potentially add google oath later
    }


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