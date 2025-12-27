import pytest 


def test_app_creation(app):
    assert app is not None
    print(app.config)
    assert app.config['TESTING'] is True

def test_app_config(app):
    assert app.config['SECRET_KEY'] is not None
    assert app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///')
    assert app.config['SESSION_COOKIE_SAMESITE'] == 'Strict'
    # assert app.config['SESSION_COOKIE_HTTPONLY'] is True
    assert app.config['FLASK_ADMIN_SWATCH'] == 'spacelab'
    assert app.config['FLASK_ADMIN'] == 'jvrezendemoura@gmail.com'
