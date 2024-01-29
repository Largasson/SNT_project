from flask import Blueprint, render_template

blueprint = Blueprint('contacts', __name__)


@blueprint.route('/contacts')
def contacts():
    """ Функция перенаправляющая на страницу контактов"""
    title = 'Контакты'
    return render_template('contacts.html', page_title=title)
