from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadFileForm(FlaskForm):
    file = FileField(render_kw={'class': 'form-control'})
    submit = SubmitField(label='Загрузить', render_kw={'class': 'btn btn-info'})
