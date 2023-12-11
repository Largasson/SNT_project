from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import csv

class PhotoForm(FlaskForm):
    file = FileField()

app = Flask(__name__)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


def parsing(text_from_csv: str):
    rows = [row.strip().split(';')  for row in text_from_csv.strip().split('\n')]
    list_of_dict = []
    for value in rows[1:]:
        dict_row = dict(zip(rows[0], value))
        list_of_dict.append(dict_row)
    print(*list_of_dict, sep='\n')
    return list_of_dict


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
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.file.data
        text_from_csv = f.read().decode('cp1251')
        parsing(text_from_csv)
        return render_template('board_office.html', form=form)

    return render_template('board_office.html', form=form)


@app.route('/lk_page')
def lk_page():
    return render_template('lk_page.html')










if __name__ == '__main__':
    app.run(debug=True)




