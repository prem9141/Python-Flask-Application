"""This test the Login, Registration and Dashboard"""

from app import db
from app.db.models import User, Song
from werkzeug.security import generate_password_hash
from flask_login import current_user


def test_request_songs_upload(client):
    """This makes the songs upload page"""
    with client:
        email = 'prem@test.com'
        password = 'prem@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        assert db.session.query(User).count() == 1
        client.post('/login', data={"email": email, "password": password})
        response = client.get('/songs/upload')
        assert response.status_code == 200
        assert b"Upload Songs" in response.data
        assert current_user.email == 'prem@test.com'


def test_request_songs_upload_deny(client):
    """This makes the songs upload page"""
    with client:
        response = client.get('/songs/upload')
        assert current_user.is_anonymous
        assert response.status_code == 302
        assert "/login" in response.location


def test_request_csv_process(client):
    """This makes the songs upload page"""
    with client:
        email = 'prem@test.com'
        password = 'prem@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        client.post('/login', data={"email": email, "password": password})

        csv_file = 'tests/pytest_songs.csv'
        data = {
            'file': (open(csv_file, 'rb'), csv_file)
        }

        client.post('/songs/upload', data=data)
        assert db.session.query(Song).count() == 2

        response = client.get('/dashboard')
        assert b'Sugar (feat. Francesco Yates)' in response.data
        assert b'Down' in response.data


