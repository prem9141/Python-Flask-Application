"""This test the My Account Menu Option"""

from app import db
from app.db.models import User


def test_request_manage_profile(client, add_user):
    """This makes the user profile edit page"""
    with client:
        assert db.session.query(User).count() == 1
        user = User.query.get(1)
        assert user.about is None
        client.post('/login', data={'email': user.email, 'password': 'prem@1234'})
        response = client.post('/profile', data={"about": 'My Profile About Test'}, follow_redirects=True)
        assert b"You Successfully Updated your Profile" in response.data
        assert user.about == 'My Profile About Test'





