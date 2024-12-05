from flask import Flask, url_for, redirect, abort, make_response, render_template_string, render_template, request
from werkzeug.exceptions import HTTPException
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5  # Подключаем код 5-ой лабораторной

app = Flask(__name__)

app.secret_key = 'G2202gA20a05'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)  

@app.route("/")
@app.route("/index")
def index():
    lab1_url = url_for("lab1.lab1_main")
    lab2_url = url_for("lab2.lab2_main")
    lab3_url = url_for("lab3.lab3_main")
    lab4_url = url_for("lab4.lab4_main")
    lab5_url = url_for("lab5.lab5_main")  
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <ul>
            <li><a href="{lab1_url}">Первая лабораторная</a></li>
            <li><a href="{lab2_url}">Вторая лабораторная</a></li>
            <li><a href="{lab3_url}">Третья лабораторная</a></li>
            <li><a href="{lab4_url}">Четвертая лабораторная</a></li>
            <li><a href="{lab5_url}">Пятая лабораторная</a></li>
        </ul>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
'''.format(url_for("lab1.lab1_main"), url_for("lab2.lab2_main"), url_for("lab3.lab3_main"), url_for("lab4.lab4_main"), url_for("lab5.lab5_main"))



@app.errorhandler(400)
def bad_request(err):
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 400 - Неверный запрос</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 400</h1>
        </header>
        <p>Неверный запрос (Bad Request)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 400

@app.errorhandler(401)
def unauthorized(err):
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 401 - Неавторизован</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 401</h1>
        </header>
        <p>Неавторизованный доступ (Unauthorized)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 401

@app.errorhandler(403)
def forbidden(err):
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 403 - Доступ запрещен</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 403</h1>
        </header>
        <p>Доступ запрещен (Forbidden)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 403

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="lab1/404.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 404</h1>
        </header>
        <p>нет такой страницы, больше сюда не заходи</p>
        <img src="{path}" alt="нет такой страницы">
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
''', 404

@app.errorhandler(405)
def method_not_allowed(err):
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 405 - Метод не разрешен</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 405</h1>
        </header>
        <p>Метод не разрешен (Method Not Allowed)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 405

@app.errorhandler(500)
def internal_server_error(err):
    return "Ошибка 500: Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.", 500

if __name__ == "__main__":
    app.run(debug=True)