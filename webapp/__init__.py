from flask import Flask, render_template, flash, redirect, url_for
import io
from webapp.parsing_csv import parsing_csv
from webapp.model import db, User, FinancialData
from webapp.forms import RegistrationForm, UploadFileForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


def create_app():
    """ Основная функция проекта. Содержит в себе инициацию Flask-приложения, функции эндпоинты,
        команды инициализации БД, и логин-менеджера в контексте основного приложения."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    @app.route('/index')
    def index():
        """ Функция, отвечающая за главную страницу. Передает в функцию
                рендеринга макет главной страницы """
        title = 'Главная страница'
        return render_template('index.html', page_title=title)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ Функция, отвечающая за страницу логина. Проверяет залогинен ли пользователь.
        Если да, то возвращает на главную страницу. Если нет, то передает в функцию рендеринга
        макет страницы логина, ФОРМУ логина, а также название страницы. В самой странице, при
        получении данных из формы они перенаправляются функции process_login """
        if current_user.is_authenticated:
            return redirect(url_for('board_office'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process_login', methods=['GET', 'POST'])
    def process_login():
        """ Функция обработки данных, перенаправленных со страницы логина. Проверяет,
         корректны ли данные, поступившие со страницы логина. Если нет, отправляет обратно
         на страницу логина. Если да, то проверяет совпадает ли пароль пользователя с паролем в БД.
         В случае успеха перенаправляет на страницу ЛК админа. """
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.area_number == form.area_number.data).first()
            print(user)
            if not user:
                flash('Пользователя с таким номером участка не зарегистрировано')
                return redirect(url_for('login'))
            if user and user.check_password(form.password.data):
                print(user)
                print(user.check_password(form.password.data))
                login_user(user)
                return redirect(url_for('lk_page', area=form.area_number.data))
        flash('Неверный номер участка или пароль')
        return redirect(url_for('login'))


    @app.route('/logout')
    def logout():
        """ Функция разлогина для пользователя. Осуществляет выход их ЛК"""
        logout_user()
        flash('Вы вышли из личного кабинета')
        return redirect(url_for('index'))


    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        """ Функция, отвечающая за страницу регистрации"""
        title = 'Регистрация'
        registration_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=registration_form)


    @app.route('/reg_processing', methods=['POST'])
    def reg_processing():
        """ Функция перехвата данных со страницы регистрации. Если данные валидны,
        то добавляются в ЮД пользователей, в противном случае пользователь
        перенаправляется на страницу регистрации"""
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(area_number=form.area_number.data,
                            email=form.email.data,
                            phone=form.phone.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы зарегистрированы')
            return redirect(url_for('login'))
        else:
            flash('Пароли не совпадают')
            return redirect(url_for('registration'))

    @app.route('/board_office', methods=['GET', 'POST'])
    def board_office():
        """ Функция, отвечающая за страницу Правления(админ-страница). Предает в функцию рендеринга
          ФОРМУ загрузки файла, а также макет админ-страницы. Обрабатывает приходящий файл  """
        form = UploadFileForm()
        title = 'Страница Правления'
        if form.validate_on_submit():
            f = form.file.data
            text_from_csv = f.read().decode('cp1251')
            data = io.StringIO(text_from_csv)
            our_dict = parsing_csv(data)
            key_sort = list(sorted(our_dict))
            for k in key_sort:
                print(f'КЛЮЧ {k}: {our_dict[k]}')
            return render_template('board_office.html', a=form, page_title=title)
        return render_template('board_office.html', a=form, page_title=title)

    @app.route('/user/<int:area>')
    def lk_page(area):
        info = FinancialData.query.filter(FinancialData.area_number == area).first()
        """ Функция генерирующая страницу рядового пользователя"""
        title = f'Страница пользователя {area}'
        # if area == 0:
        # #     return redirect(url_for('board_office'))
        return render_template('lk_page.html', page_title=title, area=area,
                               member_fee=info.member_fee, targeted_fee=info.targeted_fee,
                               electricity_payments=info.electricity_payments,
                               published=info.published)

    @app.route('/contacts')
    def contacts():
        """ Функция перенаправляющая на страницу контактов"""
        return """Еще не написал
        """

    return app