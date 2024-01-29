from io import StringIO
from flask import Blueprint, render_template
from webapp.board_office.forms import UploadFileForm
from webapp.board_office.parsing_csv import parsing_csv

blueprint = Blueprint('board_office', __name__)


@blueprint.route('/board_office', methods=['GET', 'POST'])
def board_office():
    """ Функция, отвечающая за страницу Правления(админ-страница). Предает в функцию рендеринга
      ФОРМУ загрузки файла, а также макет админ-страницы. Обрабатывает приходящий файл  """
    form = UploadFileForm()
    title = 'Страница Правления'
    if form.validate_on_submit():
        f = form.file.data
        text_from_csv = f.read().decode('cp1251')
        data = StringIO(text_from_csv)
        our_dict = parsing_csv(data)
        key_sort = list(sorted(our_dict))
        for k in key_sort:
            print(f'КЛЮЧ {k}: {our_dict[k]}')
        return render_template('board_office.html', a=form, page_title=title)
    return render_template('board_office.html', a=form, page_title=title)
