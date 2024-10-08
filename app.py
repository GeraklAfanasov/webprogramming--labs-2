from flask import Flask, url_for, redirect, abort, make_response, render_template_string, render_template, request
from werkzeug.exceptions import HTTPException

class PaymentRequired(HTTPException):
    code = 402
    description = "Необходима оплата (Payment Required)"  # 402 нестандартная ошибка


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    lab1_url = url_for("lab1")
    lab2_url = url_for("lab2")
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
            <li><a href="{lab2_url}">Вторая лабораторная</a></li>
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
    routes = [
        ('lab1', url_for('lab1')),
        ('Автор', url_for('author')),
        ('Web', url_for('start')),
        ('Счетчик', url_for('counter')),
        ('Сброс счетчика', url_for('reset_counter')),
        ('Info', url_for('info')),
        ('Oak', url_for('oak')),
        ('Created', url_for('created')),
        ('Custom Page', url_for('custom_page')),
        ('Ошибка 400', url_for('error_400')),
        ('Ошибка 401', url_for('error_401')),
        ('Ошибка 402', url_for('error_402')),
        ('Ошибка 403', url_for('error_403')),
        ('Ошибка 404', url_for('error_404')),
        ('Ошибка 405', url_for('error_405')),
        ('Ошибка 500', url_for('error_500')),
    ]
    table_rows = ''.join([f'<tr><td>{name}</td><td><a href="{url}" style="color: blue;">{url}</a></td></tr>' for name, url in routes])
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <style>
            body {{
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #000080;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            a {{
                color: blue;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Лабораторная 1</h1>
        </header>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2.
        </p>
        <a href="{root_url}" style="color: blue;">Вернуться на главную</a>
        <h2>Список роутов</h2>
        <table>
            <thead>
                <tr>
                    <th>Название маршрута</th>
                    <th>Ссылка</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
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



@app.route('/custom-page')
def custom_page():
    # Путь к картинке
    image_url = url_for('static', filename='Flask.png')
    # Текст для страницы
    page_content = '''
    <!doctype html>
    <html>
        <head>
            <title>Кастомная страница</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                }}
                .content {{
                    margin: 20px;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Добро пожаловать на кастомную страницу</h1>
            </header>
            <div class="content">
                <p>
                    Это пример страницы, которая демонстрирует работу с несколькими
                    абзацами текста. Веб-разработка может быть увлекательной и интересной, особенно
                    когда вы создаете что-то новое и функциональное.
                </p>
                <p>
                    Flask является мощным и гибким микрофреймворком для создания веб-приложений
                    на Python. Он предоставляет разработчикам возможность быстро и эффективно создавать
                    веб-сервисы, не перегружая их сложными библиотеками.
                </p>
                <p>
                    Помимо работы с текстом, веб-страницы часто содержат изображения, которые
                    делают их более привлекательными для пользователей. В нашем случае это пример
                    изображения ниже:
                </p>
                <img src="{image_url}" alt="Пример изображения">
                <p>
                    Этот текст демонстрирует работу с несколькими абзацами и изображениями,
                    а также добавление кастомных заголовков в ответ сервера.
                </p>
            </div>
            <footer>
                <p>ФИО: Афанасов Геракл Георгиевич</p>
                <p>Группа: ФБИ-22</p>
                <p>Год: 2023</p>
            </footer>
        </body>
    </html>
    '''.format(image_url=image_url)

    # Создаем ответ и добавляем заголовки
    response = make_response(page_content)
    
    # Добавляем заголовок Content-Language
    response.headers['Content-Language'] = 'ru'
    
    # Добавляем два своих нестандартных заголовка
    response.headers['X-Custom-Header-1'] = 'MyCustomHeaderValue1'
    response.headers['X-Custom-Header-2'] = 'MyCustomHeaderValue2'

    return response




#Обработчики ошибок

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


@app.route('/error500')
def error_500():
    result = 1 / 0  
    return str(result)

# Перехватчик для ошибки 500 с сообщением на русском языке
@app.errorhandler(500)
def internal_server_error(err):
    return "Ошибка 500: Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.", 500












@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'


flowers = [
    {"name": "Роза", "price": 100},
    {"name": "Тюльпан", "price": 70},
    {"name": "Подсолнух", "price": 50},
    {"name": "Лилия", "price": 80}
]

@app.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])
        flowers.append({"name": name, "price": price})
        return redirect(url_for('list_flowers'))
    return render_template('add_flower.html')

@app.route('/lab2/flowers')
def list_flowers():
    return render_template('list_flowers.html', flowers=flowers)

@app.route('/lab2/flowers/<int:flower_id>')
def flower(flower_id):
    if 0 <= flower_id < len(flowers):
        return render_template('flower.html', flower=flowers[flower_id], flowers=flowers)
    return 'Нет такого цветка', 404

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flowers
    flowers = []
    return redirect(url_for('list_flowers'))

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flowers):
        del flowers[flower_id]
        return redirect(url_for('list_flowers'))
    return 'Нет такого цветка', 404



@app.route('/lab2/')
def lab2():
    name = 'Афанасов Геракл'
    lab_num = '2'
    curs_num = '3'
    group = 'ФБИ-22'
    fruits = [
        {'name': 'Яблоко', 'price': 100},
        {'name': 'Банан', 'price': 70},
        {'name': 'Апельсин', 'price': 120},
        {'name': 'Манго', 'price': 200}
    ]
    return render_template('lab2.html', name=name, lab_num=lab_num, curs_num=curs_num, group=group, fruits=fruits)

@app.route('/lab2/filter')
def filter_example():
    phrase = "сколько нам открытий чудных готовит просвещенья дух"
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    sum_result = a + b
    diff_result = a - b
    prod_result = a * b
    div_result = a / b if b != 0 else 'Ошибка: деление на ноль'
    pow_result = a ** b
    return render_template('calc.html', a=a, b=b, sum_result=sum_result, diff_result=diff_result, prod_result=prod_result, div_result=div_result, pow_result=pow_result)




@app.route('/lab2/books')
def list_books():
    books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Научная фантастика", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 158},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 448},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 448},
    {"author": "Роберт Грин", "title": "48 законов власти", "genre": "Саморазвитие", "pages": 496},
    {"author": "Стивен Кинг", "title": "Оно", "genre": "Ужасы", "pages": 1138},
    {"author": "Агата Кристи", "title": "Убийство в Восточном экспрессе", "genre": "Детектив", "pages": 256}
    ]
    return render_template('books.html', books=books)




@app.route('/lab2/berries')
def list_berries():
    berries = [
    {"name": "Клубника", "description": "Сладкая и сочная ягода, популярная в десертах.", "image": "strawberry.jpg"},
    {"name": "Черника", "description": "Меньше по размеру, чем Голубика, но с более интенсивным вкусом.", "image": "blueberry.jpg"},
    {"name": "Ежевика", "description": "Спелая ежевика имеет сладкий вкус и используется в варенье и компотах.", "image": "blackberry.png"},
    {"name": "Голубика", "description": "Богатая антиоксидантами ягода, используемая в салатах и десертах.", "image": "cranberry.jpg"},
    {"name": "Малина", "description": "Сладкая и кислая ягода, популярная в десертах и напитках.", "image": "raspberry.jpg"}
    ]
    return render_template('berries.html', berries=berries)
if __name__ == "__main__":
    app.run(debug=True)