from flask import Flask, Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__, template_folder='templates')

@lab9.route('/lab9/')
def index():
    return render_template('lab9/index.html')