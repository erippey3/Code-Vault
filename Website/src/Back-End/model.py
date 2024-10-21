from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    # Table fields
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password
    verified = db.Column(db.Boolean, default=False, nullable=False)  # Verification status, default False
    verification_code = db.Column(db.String(128), nullable=True)  # Code for email verification
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of user creation

    def __repr__(self):
        return f'<User {self.username}>'
