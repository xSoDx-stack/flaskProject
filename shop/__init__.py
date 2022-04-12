from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer
from shop.cfg import Configuration
from flask_mail import Mail
from flask_migrate import Migrate
from os import getenv
import hashlib

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

serialize = URLSafeTimedSerializer(secret_key=getenv('TOKEN_SECRET_KEY'), salt=getenv('TOKEN_SALT'),
                                   signer_kwargs={"digest_method": hashlib.sha512})
ser_user = URLSafeSerializer(secret_key=getenv('TOKEN_SECRET_KEY'), salt=getenv('TOKEN_SALT'),
                             signer_kwargs={"digest_method": hashlib.sha512})


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    from shop.auth import auth
    from shop.administration import admin
    from shop.errors import error_bp
    from shop.seller import seller
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_perefix='/admin')
    app.register_blueprint(seller, url_prefix='/seller')
    app.register_blueprint(error_bp)
    return app


app = create_app()
from shop.view import *
