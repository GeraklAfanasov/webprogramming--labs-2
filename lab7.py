from flask import Blueprint, render_template, request, jsonify, session, current_app
from lab5 import get_db_connection, close_db_connection
import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():  # Изменили имя функции с main на lab
    return render_template('lab7/lab7.html')