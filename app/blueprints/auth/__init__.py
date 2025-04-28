from flask import Blueprint
from .views.login import blueprint as login
from .views.logout import blueprint as logout
from .views.registration import blueprint as registration

# Создаём основной Blueprint для auth
blueprint = Blueprint('auth', __name__)

# Регистрируем отдельные вьюхи
blueprint.register_blueprint(login, url_prefix='/auth')
blueprint.register_blueprint(logout, url_prefix='/auth')
blueprint.register_blueprint(registration, url_prefix='/auth')
