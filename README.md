# SNT_project
SNT_project - вэб-приложения для СНТ, которое позволит каждому владельцу участка 
иметь свой личный кабинет в котором будет отражаться информация о состоянии его 
счета: задолжности и/или переплате по членским и целевым взносам. Добавление бухгалтерской 
информации осуществляется из личного кабинета Правления. 

### Установка
1. Клонировать репозиторий и создать виртуальное окружение:
```
git clone https://github.com/Largasson/SNT_project
```
2. Установить зависимости - требуемые библиотеки для работы веб-приложения:
```
pip install -r requirements.txt
```
4. Создать файл __.env__ с переменными окружения: 
```
FLASK_APP=webapp
FLASK_ENV=development
SECRET_KEY="Пароль"
WTF_CSRF_SECRET_KEY="Секретный ключ"
```
5. Запустить файл __create_db.py__ для создания БД.
6. Запустить приложение командой в терминале flask run