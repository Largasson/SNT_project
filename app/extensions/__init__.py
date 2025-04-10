from .db import db
from .login_manager import login_manager
from app.models import User

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)