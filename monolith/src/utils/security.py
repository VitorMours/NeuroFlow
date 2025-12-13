from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, g, request, session, flash
from functools import wraps
from markupsafe import escape
import re
salt = 16

def encrypt_password(password: str) -> str:
    global salt
    encrypt_password = generate_password_hash(password, "scrypt", salt)
    return encrypt_password

def check_password(password: str, hashed_password: str) -> str:
    password_validation = check_password_hash(hashed_password, password)
    return password_validation

def email_validator(email: str) -> bool:
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(EMAIL_REGEX, email) is not None


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("login"):
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("views.auth.login"))
        return view(*args, **kwargs)
    return wrapped_view


def sanitize_request(view):
    """
    This function is responsible for sanitizing the request
    in a way that the data is more clean and easy to work with on
    Returns:
    --------
        g.sanitized_request: dict
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        sanitized = {}

        if request.form:
            sanitized.update({k: escape(v) for k, v in request.form.items()})

        g.sanitized_request = sanitized
        return view(*args, **kwargs)
    return wrapped_view
