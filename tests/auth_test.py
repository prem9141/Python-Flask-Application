"""This test the Login, Registration and Dashboard"""

from app import db
from app.db.models import User, Song
from werkzeug.security import generate_password_hash
from flask_login import current_user


def test_request_login(client):
    """This makes the valid user login page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem@test.com'
        password = 'prem@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        assert db.session.query(User).count() == 1
        response = client.post('/login', data={"email": email, "password": password}, follow_redirects=True)
        assert b"Welcome" in response.data
        assert current_user.email == 'prem@test.com'


def test_request_login_fail_user(client):
    """This makes the invalid user login page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem@test.com'
        password = 'prem@1234'
        response = client.post('/login', data={"email": email, "password": password}, follow_redirects=True)
        assert b"Invalid username or password" in response.data
        assert current_user.is_anonymous


def test_request_login_fail_user_password(client):
    """This makes the valid user but invalid password login page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem2@test.com'
        password = 'prem2@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        assert db.session.query(User).count() == 1
        response = client.post('/login', data={"email": email, "password": "prem@1234"}, follow_redirects=True)
        assert b"Invalid username or password" in response.data
        assert current_user.is_anonymous


def test_request_register(client):
    """This makes the user registration page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem@test.com'
        password = 'prem@1234'
        response = client.post('/register', data={"email": email, "password": password, "confirm": password},
                               follow_redirects=True)
        assert db.session.query(User).count() == 1
        assert b"Congratulations, you are now a registered user" in response.data


def test_request_register_already(client):
    """This makes the user registration page: user registered already"""
    with client:
        email = 'prem@test.com'
        password = 'prem@1234'
        user = User(email, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        assert db.session.query(User).count() == 1
        response = client.post('/register', data={"email": email, "password": password, "confirm": password},
                               follow_redirects=True)
        assert db.session.query(User).count() == 1
        assert b"Already Registered" in response.data

