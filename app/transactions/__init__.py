import csv
import os
import logging
from datetime import datetime as dt

from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transaction
from app.transactions.forms import csv_upload
from app.auth.decorators import admin_required
from werkzeug.utils import secure_filename, redirect

transactions = Blueprint('transactions', __name__,
                        template_folder='templates')
mytransaction = logging.getLogger("myTransaction")


@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
@login_required
@admin_required
def transactions_browse(page):
    page = page
    per_page = 15
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('user_id', 'User ID'), ('tdate', 'Transaction Upload DateTime'), ('ttype', 'Transaction Type'),
              ('amount', 'Amount')]
    try:
        return render_template('browse_transactions.html', data=data, titles=titles, pagination=pagination,
                               record_type="Transactions")
    except TemplateNotFound:
        abort(404)


@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    form = csv_upload()
    if form.validate_on_submit():

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)

        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                current_user.transactions.append(Transaction(abs(int(row['AMOUNT'])), row['TYPE']))
                db.session.commit()
        current_time = dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        mytransaction.info(f'File {filename} uploaded by user {current_user.email} at time {current_time}')

        return redirect(url_for('auth.dashboard'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
