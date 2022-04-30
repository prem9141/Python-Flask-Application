import logging

from app import db
from app.db.models import User, Song


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


def test_adding_songs(application):
    assert db.session.query(Song).count() == 0
    assert db.session.query(User).count() == 0

    user = User('prem@gmail.com', 'prem@1234')
    db.session.add(user)
    db.session.commit()

    user = User.query.get(1)
    assert user.email == 'prem@gmail.com'
    assert db.session.query(User).count() == 1

    user.songs = [Song("title_1", "artist_1", "genre_1", 2022), Song("title_2", "artist_2", "genre_2", 2021)]

    assert db.session.query(Song).count() == 2

    song1 = Song.query.filter_by(title='title_1').first()
    assert song1.artist == 'artist_1'

    song2 = Song.query.filter_by(title='title_2').first()
    assert song2.artist == 'artist_2'

    db.session.delete(user)
    db.session.delete(song1)
    db.session.delete(song2)

    assert db.session.query(User).count() == 0
    assert db.session.query(Song).count() == 0





