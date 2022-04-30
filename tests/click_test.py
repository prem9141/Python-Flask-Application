import os
from click.testing import CliRunner
from app.cli import create_database
from app import config
runner = CliRunner()


def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0

    root = config.Config.BASE_DIR
    dbdir = os.path.join(root, '..', config.Config.DB_DIR)

    assert os.path.exists(dbdir)