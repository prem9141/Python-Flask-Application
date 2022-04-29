"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name

import pytest
from app import create_app, User
import os
import logging
from app.db import db


@pytest.fixture()
def application():
    """This makes the app"""
    os.environ['FLASK_ENV'] = 'testing'
    application = create_app()
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()
