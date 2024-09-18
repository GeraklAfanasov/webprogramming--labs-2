from flask import Flask, url_for, redirect, abort
from werkzeug.exceptions import HTTPException

class PaymentRequired(HTTPException):
    code = 402
    description = "Необходима оплата (Payment Required)" #без явного создания класса будет выходить ошибка, ведь 402 - нестандартная ошибка


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    lab1_url = url_for("start")
    css_path = url_for("static", filename="lab1.css")
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
        </ul>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="lab1.css")
    root_url = url_for("index")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Лабораторная 1</h1>
        </header>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="{root_url}">Вернуться на главную</a>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
'''



@app.route("/lab1/web")
def start():
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html> 
    <html> 
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header>
                <h1>web-сервер на flask</h1>
            </header>
            <footer>
                <p>ФИО: Афанасов Геракл Георгиевич</p>
                <p>Группа: ФБИ-22</p>
                <p>Курс: 2</p>
                <p>Год: 2023</p>
            </footer>
        </body> 
    </html>''', 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@app.route("/lab1/author")
def author():
    name = "Афанасов Геракл Георгиевич"
    group = "ФБИ-22"
    faculty = "ФБ"
    css_path = url_for("static", filename="lab1.css")
    return f'''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <header>
                    <h1>Студент</h1>
                </header>
                <p>Студент: {name}</p>
                <p>Группа: {group}</p>
                <p>Факультет: {faculty}</p>
                <a href="{url_for('start')}">web</a>
                <footer>
                    <p>ФИО: Афанасов Геракл Георгиевич</p>
                    <p>Группа: ФБИ-22</p>
                    <p>Курс: 2</p>
                    <p>Год: 2023</p>
                </footer>
            </body>
        </html>'''

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Дуб</h1>
        </header>
        <img src="{path}" alt="Дуб">
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>    
'''

count = 0

@app.route("/lab1/counter")
def counter():
    global count  
    count += 1
    reset_url = url_for("reset_counter")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html> 
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Счетчик посещений</h1>
        </header>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <a href="{reset_url}">Очистить счетчик</a>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count 
    count = 0 
    counter_url = url_for("counter")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html> 
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Счетчик очищен</h1>
        </header>
        <p>Счетчик был сброшен.</p>
        <a href="{counter_url}">Вернуться к счетчику</a>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect(url_for("author"))

@app.route("/created")
def created():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Создано успешно</h1>
        </header>
        <div><i>что-то созданно ...</i></div>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
''', 201

@app.errorhandler(400)
def bad_request(err):
    css_path = url_for("static", filename="lab1.css")
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
    css_path = url_for("static", filename="lab1.css")
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

@app.errorhandler(PaymentRequired)
def payment_required(err):
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 402 - Необходима оплата</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 402</h1>
        </header>
        <p>Необходима оплата (Payment Required)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 402


@app.errorhandler(403)
def forbidden(err):
    css_path = url_for("static", filename="lab1.css")
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
    path = url_for("static", filename="404.jpg")
    css_path = url_for("static", filename="lab1.css")
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
    css_path = url_for("static", filename="lab1.css")
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

@app.errorhandler(418)
def im_a_teapot(err):
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 418 - Я чайник</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>
            <h1>Ошибка 418</h1>
        </header>
        <p>Я чайник (I'm a teapot)</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
        </footer>
    </body>
</html>
''', 418

@app.route('/error400')
def error_400():
    abort(400)  # Вызов ошибки 400

@app.route('/error401')
def error_401():
    abort(401)  # Вызов ошибки 401

@app.route('/error402')
def error_402():
    raise PaymentRequired()  # Вызов ошибки 402 через созданный класс

@app.route('/error403')
def error_403():
    abort(403)  # Вызов ошибки 403

@app.route('/error404')
def error_404():
    abort(404)  # Вызов ошибки 404

@app.route('/error405')
def error_405():
    abort(405)  # Вызов ошибки 405



if __name__ == "__main__":
    app.run(debug=True)