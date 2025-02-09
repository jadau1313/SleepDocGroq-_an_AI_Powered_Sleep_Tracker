from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


import os

db = SQLAlchemy()
migrate = Migrate()
login_mgr = LoginManager()
login_mgr.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_mgr.init_app(app)
    migrate.init_app(app, db)

    from sleep_tracker.routes.auth import auth
    from sleep_tracker.routes.sleep_log import sleep_log
    from sleep_tracker.routes.dashboard import dashboard
    from sleep_tracker.routes.main import main

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(sleep_log, url_prefix="/sleep_log")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)

    return app
@login_mgr.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
