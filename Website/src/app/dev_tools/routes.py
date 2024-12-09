from flask import jsonify, render_template, request, session
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db, es  # Your SQLAlchemy and Elasticsearch instances
from app.model import User, Project, Tag, ProjectTag
from . import dev_tools

@dev_tools.route('/delete_db', methods=['GET', 'DELETE'])
@login_required
def delete_databases():
    # if not current_user.is_authenticated or not current_user.username == 'admin':
    #     return jsonify({"error": "Unauthorized access"}), 403
    if request.method == 'DELETE':
        try:
            # Step 1: Clear all SQLAlchemy tables
            db.session.query(ProjectTag).delete()  # Clear ProjectTag table
            db.session.query(Tag).delete()        # Clear Tag table
            db.session.query(Project).delete()    # Clear Project table
            db.session.query(User).delete()       # Clear User table
            db.session.commit()

            # Step 2: Delete all documents from Elasticsearch
            es.indices.delete(index="projects_index", ignore=[400, 404])  # Ignore errors if index doesn't exist

            session.clear()
            return jsonify({"message": "All data cleared successfully!"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the transaction in case of error
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    return render_template('main.html')

@dev_tools.route('/clear_session', methods=['GET'])
def clear_session():
    session.clear()
    return jsonify({"message": "Session Cleared successfully!"}), 200