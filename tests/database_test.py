import logging

from app import db
from app.db.models import User, Transaction


def test_adding_user(application):
        assert db.session.query(User).count() == 0
        user = User('prem@gmail.com', 'prem@1234')
        db.session.add(user)
        db.session.commit()

        assert db.session.query(User).count() == 1

        user = User.query.get(1)
        assert user.email == 'prem@gmail.com'


def test_deleting_user(application):
        assert db.session.query(User).count() == 0
        user = User('prem@gmail.com', 'prem@1234')
        db.session.add(user)
        db.session.commit()

        assert db.session.query(User).count() == 1

        user = User.query.get(1)
        assert user.email == 'prem@gmail.com'

        db.session.delete(user)
        assert db.session.query(User).count() == 0


def test_adding_transactions(application):
    assert db.session.query(Transaction).count() == 0
    assert db.session.query(User).count() == 0

    user = User('prem@gmail.com', 'prem@1234')
    db.session.add(user)
    db.session.commit()

    user.transactions = [Transaction(1000, 'DEBIT'), Transaction(2000, 'CREDIT')]

    assert db.session.query(Transaction).count() == 2

    debit = Transaction.query.filter_by(ttype='DEBIT').first()
    assert debit.amount == 1000
    assert debit.user_id == 1

    credit = Transaction.query.filter_by(ttype='CREDIT').first()
    assert credit.amount == 2000
    assert credit.user_id == 1

    db.session.delete(user)
    db.session.delete(debit)
    db.session.delete(credit)

    assert db.session.query(User).count() == 0
    assert db.session.query(Transaction).count() == 0





