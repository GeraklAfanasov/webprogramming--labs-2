from flask import Blueprint, url_for, redirect, abort, make_response, render_template, request
from werkzeug.exceptions import HTTPException

lab1 = Blueprint('lab1', __name__)

class PaymentRequired(HTTPException):
    code = 402
    description = "Необходима оплата (Payment Required)"  # 402 нестандартная ошибка

@lab1.route("/lab1")
def lab1_main():
    css_path = url_for("static", filename="lab1/main.css")
    root_url = url_for("index")
    routes = [
        ('lab1', url_for('lab1.lab1_main')),
        ('Автор', url_for('lab1.author')),
        ('Web', url_for('lab1.start')),
        ('Счетчик', url_for('lab1.counter')),
        ('Сброс счетчика', url_for('lab1.reset_counter')),
        ('Info', url_for('lab1.info')),
        ('Oak', url_for('lab1.oak')),
        ('Created', url_for('lab1.created')),
        ('Custom Page', url_for('lab1.custom_page')),
        ('Ошибка 400', url_for('lab1.error_400')),
        ('Ошибка 401', url_for('lab1.error_401')),
        ('Ошибка 402', url_for('lab1.error_402')),
        ('Ошибка 403', url_for('lab1.error_403')),
        ('Ошибка 404', url_for('lab1.error_404')),
        ('Ошибка 405', url_for('lab1.error_405')),
        ('Ошибка 500', url_for('lab1.error_500')),
    ]
    return render_template('lab1/lab1.html', css_path=css_path, root_url=root_url, routes=routes)

@lab1.route("/lab1/web")
def start():
    css_path = url_for("static", filename="/lab1/lab1.css")
    return render_template('/lab1/start.html', css_path=css_path), 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@lab1.route("/lab1/author")
def author():
    name = "Афанасов Геракл Георгиевич"
    group = "ФБИ-22"
    faculty = "ФБ"
    css_path = url_for("static", filename="/lab1/lab1.css")
    return render_template('/lab1/author.html', name=name, group=group, faculty=faculty, css_path=css_path)

@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/main.css")
    return render_template('lab1/oak.html', path=path, css_path=css_path)

count = 0

@lab1.route("/lab1/counter")
def counter():
    global count  
    count += 1
    reset_url = url_for("lab1.reset_counter")
    css_path = url_for("static", filename="lab1/main.css")
    return render_template('lab1/counter.html', count=count, reset_url=reset_url, css_path=css_path)

@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count 
    count = 0 
    counter_url = url_for("lab1.counter")
    css_path = url_for("static", filename="lab1/main.css")
    return render_template('lab1/reset_counter.html', counter_url=counter_url, css_path=css_path)

@lab1.route("/lab1/info")
def info():
    return redirect(url_for("lab1.author"))

@lab1.route("/created")
def created():
    css_path = url_for("static", filename="lab1/main.css")
    return render_template('lab1/created.html', css_path=css_path), 201

@lab1.route('/custom-page')
def custom_page():
    # Путь к картинке
    image_url = url_for('static', filename='lab1/Flask.png')
    # Текст для страницы
    page_content = render_template('lab1/custom_page.html', image_url=image_url)

    # Создаем ответ и добавляем заголовки
    response = make_response(page_content)
    
    # Добавляем заголовок Content-Language
    response.headers['Content-Language'] = 'ru'
    
    # Добавляем два своих нестандартных заголовка
    response.headers['X-Custom-Header-1'] = 'MyCustomHeaderValue1'
    response.headers['X-Custom-Header-2'] = 'MyCustomHeaderValue2'

    return response

@lab1.route('/error400')
def error_400():
    abort(400)  # Вызов ошибки 400

@lab1.route('/error401')
def error_401():
    abort(401)  # Вызов ошибки 401

@lab1.route('/error402')
def error_402():
    raise PaymentRequired()  # Вызов ошибки 402 через созданный класс

@lab1.route('/error403')
def error_403():
    abort(403)  # Вызов ошибки 403

@lab1.route('/error404')
def error_404():
    abort(404)  # Вызов ошибки 404

@lab1.route('/error405')
def error_405():
    abort(405)  # Вызов ошибки 405

@lab1.route('/error500')
def error_500():
    result = 1 / 0  
    return str(result)