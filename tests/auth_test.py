"""This test the Login, Registration and Dashboard"""

from app import db
from app.db.models import User, Song
from werkzeug.security import generate_password_hash


def test_request_login(client):
    """This makes the valid login page"""
    with client:
        email = 'prem@test.com'
        password = 'prem@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        assert db.session.query(User).count() == 1
        client.post('/login', data={"email": email, "password": password})
        response = client.get('/dashboard')
        assert response.status_code == 200


def test_request_login_fail_user(client):
    """This makes the invalid login user page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem@test.com'
        password = 'prem@1234'
        client.post('/login', data={"email": email, "password": password})
        response = client.get('/dashboard')
        assert response.status_code == 302
