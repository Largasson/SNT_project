from io import StringIO
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired
from app.extensions.logger import logger


class UploadFileForm(FlaskForm):
    """
    Форма для загрузки файла.
    """
    file = FileField(
        label="Выберите файл",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField(
        label="Загрузить",
        render_kw={"class": "btn btn-info"},
    )

    def convert_file_field_data_to_csv_file(self):
        """
        Преобразует содержимое загруженного файла в CSV-формат.

        :raises ValueError: Если произошла ошибка при декодировании файла.
        :return: StringIO объект с данными файла.
        """
        try:
            f = self.file.data
            text_from_csv = f.read().decode("cp1251")
            logger.info("Файл успешно прочитан и сконвертирован в CSV.")
            return StringIO(text_from_csv)
        except Exception as e:
            logger.error(f"Ошибка при конвертации файла: {e}")
            raise ValueError(f"Ошибка при обработке файла: {str(e)}")


class NewsForm(FlaskForm):
    """
    Форма для добавления новостей.
    """
    news_title = StringField(
        label="Заголовок новости",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    news_content = TextAreaField(
        label="Содержание новости",
        render_kw={"class": "form-control"},
    )
    submit = SubmitField(
        label="Опубликовать",
        render_kw={"class": "btn btn-info"},
    )
