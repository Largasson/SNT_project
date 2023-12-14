from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
import csv
import io
from flask_sqlalchemy import SQLAlchemy

import settings


class UplaudFileForm(FlaskForm):

    file = FileField(render_kw={'class': 'form-control'})
    Загрузить = SubmitField(render_kw={'class': 'btn btn-info'})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.KEY_DB
db = SQLAlchemy(app)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/log_in')
def log_in():
    return render_template('log_in.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/board_office', methods=['GET', 'POST'])
def board_office():
    form = UplaudFileForm()

    if form.validate_on_submit():
        f = form.file.data
        text_from_csv = f.read().decode('cp1251')
        data = io.StringIO(text_from_csv)
        our_dict = csv.DictReader(data, delimiter=';')         # словарь для БД
        for row in our_dict:
            print(row)

        return render_template('board_office.html', a=form)
    return render_template('board_office.html', a=form)


@app.route('/lk_page')
def lk_page():
    return render_template('lk_page.html')


if __name__ == '__main__':
    app.run(debug=True)
