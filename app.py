from flask import Flask, url_for, redirect

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

@app.errorhandler(404)
def not_found(err):
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
        <p>нет такой страницы</p>
        <footer>
            <p>ФИО: Афанасов Геракл Георгиевич</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2023</p>
        </footer>
    </body>
</html>
''', 404

if __name__ == "__main__":
    app.run(debug=True)