from .extensions import db
from datetime import datetime

# v 1.1
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    github_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
# v 1.2
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(120), unique=True, nullable=False)
    language = db.Column(db.String(16), nullable=False)

    # A JSON field for metadata if using PostgreSQL or MySQL 5.7+ could be:
    # metadata = db.Column(db.JSON, nullable=True)

    project_tags_association = db.relationship("ProjectTag", back_populates="project")
    tags = db.relationship("Tag", secondary="project_tags", back_populates="projects")

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, nullable=False)

    tag_projects_association = db.relationship("ProjectTag", back_populates="tag")
    projects = db.relationship("Project", secondary="project_tags", back_populates="tags")


class ProjectTag(db.Model):
    __tablename__ = "project_tags"
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    # Relationships (optional but recommended)
    project = db.relationship("Project", back_populates="project_tags_association")
    tag = db.relationship("Tag", back_populates="tag_projects_association")




