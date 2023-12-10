from flask import Flask, render_template


app = Flask(__name__)

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


@app.route('/board_office')
def board_office():
    return render_template('board_office.html')


@app.route('/lk_page')
def lk_page():
    return render_template('lk_page.html')


if __name__ == '__main__':
    app.run(debug=True)


