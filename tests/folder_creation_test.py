import os
from click.testing import CliRunner
from app.cli import create_database
from app import config
runner = CliRunner()


def test_create_database():
    """ This tests the database folder creation"""
    response = runner.invoke(create_database)
    assert response.exit_code == 0

    root = config.Config.BASE_DIR
    dbdir = os.path.join(root, '..', config.Config.DB_DIR)

    assert os.path.exists(dbdir)


def test_create_uploads():
    """ This tests the upload folder creation"""

    updir = config.Config.UPLOAD_FOLDER
    assert os.path.exists(updir)


def test_create_logs():
    """ This tests the logs folder creation"""

    logdir = config.Config.LOG_DIR
    assert os.path.exists(logdir)

