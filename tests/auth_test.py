"""This test the Login, Registration and Dashboard"""

from app import db
from app.db.models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user


def test_request_login(client, add_user):
    """This makes the valid user login page"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        response = client.post('/login', data={"email": user.email, "password": 'prem@1234'}, follow_redirects=True)
        assert b"Welcome" in response.data
        assert current_user.email == 'prem@gmail.com'


def test_request_login_fail_user_email(client):
    """This makes the invalid user login page"""
    with client:
        assert db.session.query(User).count() == 0
        email = 'prem@test.com'
        response = client.post('/login', data={"email": email, "password": 'prem@1234'}, follow_redirects=True)
        assert b"Invalid username or password" in response.data
        assert current_user.is_anonymous


def test_request_login_fail_user_password(client, add_user):
    """This makes the valid user but invalid password login page"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        response = client.post('/login', data={"email": user.email, "password": "prm@1234"}, follow_redirects=True)
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


def test_request_register_already(client, add_user):
    """This makes the user registration page: user registered already"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        response = client.post('/register', data={"email": user.email, "password": 'password', "confirm": 'password'},
                               follow_redirects=True)
        assert b"Already Registered" in response.data


def test_request_dashboard(client, add_user):
    """This makes the user dashboard page"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        client.post('/login', data={"email": user.email, "password": 'prem@1234'})
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b"Current Balance: $0.00" in response.data
        assert current_user.email == 'prem@gmail.com'


def test_request_dashboard_deny(client):
    """This makes the user dashboard page deny access"""
    with client:
        response = client.get('/dashboard')
        assert current_user.is_anonymous
        assert response.status_code == 302
        assert "/login" in response.location



