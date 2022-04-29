from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import Pagination

from werkzeug.security import generate_password_hash

from app.auth.forms import login_form, register_form, profile_edit_form, user_edit_form, password_update_form
from app.db import db
from app.db.models import User
from app.auth.decorators import admin_required

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if form.validate_on_submit():
        print(request.form)
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome", 'success')
            return redirect(url_for('auth.dashboard'))
    return render_template('login.html', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('auth.login'), 302)
        else:
            flash('Already Registered', 'info')
            return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)

@auth.route('/dashboard', methods=['GET'], defaults ={"page": 1})
@auth.route('/dashboard/<int:page>', methods=['GET'])
@login_required
def dashboard(page):

    songs = current_user.songs

    page = page
    per_page = 10
    pagination = Pagination(None, page, per_page, len(songs), None)

    start = (page - 1) * per_page
    end = start + per_page
    data = songs[start:end]

    titles = [('title', 'Title'), ('artist', 'Artist'), ('genre', 'Genre'), ('year', 'Year')]
    return render_template('dashboard.html', data=data, titles=titles, pagination=pagination)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('auth.retrieve_user', [('user_id', ':id')])
    edit_url = ('auth.edit_user', [('user_id', ':id')])
    add_url = url_for('auth.add_user')
    delete_url = ('auth.delete_user', [('user_id', ':id')])
    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           retrieve_url=retrieve_url, data=data, User=User, record_type="Users")


@auth.route('/users/<int:user_id>')
@login_required
@admin_required
def retrieve_user(user_id):
    user = User.query.get(user_id)
    return render_template('profile_view.html', user=user)


@auth.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = user_edit_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        user.is_admin = int(form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User Edited Successfully', 'success')
        current_app.logger.info("edited a user")
        return redirect(url_for('auth.browse_users'))
    return render_template('user_edit.html', form=form)


@auth.route('/users/new', methods=['POST', 'GET'])
@login_required
@admin_required
def add_user():
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you just created a user')
            return redirect(url_for('auth.browse_users'))
        else:
            flash('Already Registered')
            return redirect(url_for('auth.browse_users'))
    return render_template('profile_new.html', form=form)


@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    logged_in_user = current_user
    if user.id == logged_in_user.id:
        flash("You can't delete yourself!")
        return redirect(url_for('auth.browse_users'), 302)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted', 'success')
    return redirect(url_for('auth.browse_users'), 302)


@auth.route('/profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    user = User.query.get(current_user.get_id())
    form = profile_edit_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Profile', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('profile_edit.html', form=form)

@auth.route('/account', methods=['POST', 'GET'])
@login_required
def edit_account():
    user = User.query.get(current_user.get_id())
    form = password_update_form(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Password or Email', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('manage_account.html', form=form)