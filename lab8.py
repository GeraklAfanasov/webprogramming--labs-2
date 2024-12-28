from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if current_user.is_authenticated:
        user = current_user.login
    else:
        user = 'Анонимус'
    return render_template('lab8/lab8.html', user=user)