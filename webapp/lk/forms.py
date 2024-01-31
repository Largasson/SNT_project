from io import StringIO
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadFileForm(FlaskForm):
    file = FileField(render_kw={'class': 'form-control'})
    submit = SubmitField(label='Загрузить', render_kw={'class': 'btn btn-info'})

    def convert_file_field_data_to_csv_file(self):
        f = self.file.data
        text_from_csv = f.read().decode('cp1251')
        return StringIO(text_from_csv)
