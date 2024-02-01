from io import StringIO
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class UploadFileForm(FlaskForm):
    file = FileField(render_kw={'class': 'form-control'})
    submit = SubmitField(label='Загрузить', render_kw={'class': 'btn btn-info'})

    def convert_file_field_data_to_csv_file(self):
        f = self.file.data
        text_from_csv = f.read().decode('cp1251')
        return StringIO(text_from_csv)



class NewsForm(FlaskForm):
    news_title = StringField('Заголовок новости', validators=[DataRequired()])
    news_content = TextAreaField('Содержание новости', render_kw={'class': 'btn btn-primary'})
    submit = SubmitField('Опубликовать')