from flask import Flask
from os import path, getenv
from dotenv import load_dotenv

load_dotenv('/.env')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    from .views import views
    from .form_data import form_data

    app.register_blueprint(form_data, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
