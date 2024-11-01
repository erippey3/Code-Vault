from functools import wraps
from flask import session, redirect, url_for, flash


#include this as a 
#@login_required above any endpoint
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function