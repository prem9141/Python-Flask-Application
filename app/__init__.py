"""A simple flask web app"""
import flask_login
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

import os
import logging
from logging.handlers import RotatingFileHandler

from app.context_processors import utility_text_processors
from app.simple_pages import simple_pages
from app.auth import auth
from app.exceptions import http_exceptions
from app.db.models import User
from app.db import db, database
from app.transactions import transactions
from app.auth import auth
from app.cli import create_database
from flask_cors import CORS
from app.logging_config import log_con, LOGGING_CONFIG

login_manager = flask_login.LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    app.register_blueprint(simple_pages)
    app.register_blueprint(auth)
    app.register_blueprint(database)

    app.register_blueprint(transactions)
    app.register_blueprint(log_con)
    app.context_processor(utility_text_processors)

    app.cli.add_command(create_database)
    db.init_app(app)

    api_v1_cors_config = {
        "methods": ["OPTIONS", "GET", "POST"],
    }
    CORS(app, resources={"/api/*": api_v1_cors_config})

    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
