from .db import db
from .login_manager import login_manager


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login.login'
