"""This test the Login, Registration and Dashboard"""

from app import db
from app.db.models import User, Transaction
from werkzeug.security import generate_password_hash
from flask_login import current_user


def test_request_transactions_upload(client, add_user):
    """This makes the transactions upload page"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        client.post('/login', data={"email": user.email, "password": 'prem@1234'})
        response = client.get('/transactions/upload')
        assert response.status_code == 200
        assert b"Upload Transactions" in response.data
        assert current_user.email == 'prem@gmail.com'


def test_request_transaction_upload_deny(client):
    """This makes the transactions upload page"""
    with client:
        response = client.get('/transactions/upload')
        assert current_user.is_anonymous
        assert response.status_code == 302
        assert "/login" in response.location


def test_request_upload_process_csv(client, add_user):
    """This makes the transactions upload page"""
    with client:
        user = User.query.get(1)
        client.post('/login', data={"email": user.email, "password": 'prem@1234'})

        csv_file = 'tests/pytest_transactions.csv'
        data = {
            'file': (open(csv_file, 'rb'), csv_file)
        }

        client.post('/transactions/upload', data=data)
        assert db.session.query(Transaction).count() == 3


def test_request_check_balance(client, add_user):
    """This makes the transactions upload page"""
    with client:
        user = User.query.get(1)
        client.post('/login', data={"email": user.email, "password": 'prem@1234'})

        csv_file = 'tests/pytest_transactions.csv'
        data = {
            'file': (open(csv_file, 'rb'), csv_file)
        }

        client.post('/transactions/upload', data=data)
        assert db.session.query(Transaction).count() == 3

        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b"Current Balance: $3900.00" in response.data
        assert current_user.email == 'prem@gmail.com'

