from webapp import db, create_app



def create_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    create_db()