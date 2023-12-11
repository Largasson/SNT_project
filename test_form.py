from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField





class PhotoForm(FlaskForm):
    file = FileField()


app_form = Flask(__name__)

app_form.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@app_form.route('/', methods=['GET', 'POST'])
@app_form.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()

    if form.validate_on_submit():
        f = form.file.data
        input_file = f.read().decode('cp1251')
        print(input_file)


        return render_template('upload.html', form=form)

    return render_template('upload.html', form=form)





if __name__ == '__main__':
    app_form.run(debug=True)