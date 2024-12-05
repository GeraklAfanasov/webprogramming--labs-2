from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'Gerakl'  # Необходимо для работы сессий

# Создание Blueprint
lab5 = Blueprint('lab5', __name__)

# Фиктивные данные для демонстрации
articles = []
users = []

@lab5.route('/lab5/')
def lab():
    """Главная страница лабораторной"""
    return render_template('lab5/lab5.html', login=session.get('login', 'anonymous'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('lab5.create'))

        flash('Неправильный логин или пароль')
    
    return render_template('lab5/login.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        users.append({'name': name, 'username': username, 'password': password})
        flash('Пользователь успешно зарегистрирован!')
        return redirect(url_for('lab5.login'))
    
    return render_template('lab5/register.html')

@lab5.route('/lab5/list')
def list_articles():
    """Страница со списком статей"""
    return render_template('lab5/list.html', articles=articles)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    """Страница создания статьи"""
    if request.method == 'POST':
        title = request.form['title']
        article_text = request.form['article_text']
        # Добавление статьи в список (в реальном приложении это было бы добавление в БД)
        articles.append({'title': title, 'article_text': article_text, 'id': len(articles) + 1})
        return redirect(url_for('lab5.list_articles'))
    return render_template('lab5/create_article.html')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    """Страница редактирования статьи"""
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        return "Статья не найдена", 404

    if request.method == 'POST':
        article['title'] = request.form['title']
        article['article_text'] = request.form['article_text']
        return redirect(url_for('lab5.list_articles'))

    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    """Удаление статьи"""
    global articles
    articles = [a for a in articles if a['id'] != article_id]
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/logout')
def logout():
    """Выход из системы"""
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))

# Регистрация Blueprint
app.register_blueprint(lab5)











# from flask import Blueprint, render_template, session

# # Создание Blueprint
# lab5 = Blueprint('lab5', __name__)

# @lab5.route('/lab5/')
# def lab():
#     """Главная страница лабораторной"""
#     return render_template('lab5/lab5.html', login=session.get('login', 'anonymous'))

# @lab5.route('/lab5/login')
# def login():
#     """Страница входа"""
#     return render_template('lab5/login.html')

# @lab5.route('/lab5/register')
# def register():
#     """Страница регистрации"""
#     return render_template('lab5/register.html')

# @lab5.route('/lab5/list')
# def list_articles():
#     """Страница со списком статей"""
#     return render_template('lab5/list.html')

# @lab5.route('/lab5/create')
# def create_article():
#     """Страница создания статьи"""
#     return render_template('lab5/create.html')














# from flask import Blueprint, render_template, request, session, redirect, current_app  
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from werkzeug.security import check_password_hash, generate_password_hash 
# import sqlite3
# from os import path

# lab5 = Blueprint('lab5', __name__)

# @lab5.route('/lab5/')
# def lab():
#     return render_template('lab5/lab5.html', login=session.get('login'))

# def db_connect():
#     if current_app.config['DB_TYPE'] == 'postgres':
#         conn = psycopg2.connect(
#             host='',
#             database='',
#             user='',
#             password=''
#         )
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#     else:
#         dir_path = path.dirname(path.realpath(__file__))
#         db_path = path.join(dir_path, "database.db")
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row 
#         cur = conn.cursor()

#     return conn, cur 

# def db_close(conn, cur):
#     conn.commit()
#     cur.close()
#     conn.close()

# @lab5.route('/lab5/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('lab5/register.html')

#     # Получаем данные из формы
#     login = request.form.get('login')
#     password = request.form.get('password')

#     # Проверка на пустые поля
#     if not login or not password:
#         return render_template('lab5/register.html', 
#                                error="Заполните все поля")

#     # Подключение к базе данных
#     try:
#         conn, cur = db_connect()
#     except Exception as e:
#         print(f"Ошибка подключения к базе данных: {e}")
#         return render_template('lab5/register.html', 
#                                error="Ошибка подключения к базе данных")

#     try:
#         # Проверка существования пользователя
#         query = "SELECT login FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT login FROM users WHERE login=?;"
#         cur.execute(query, (login,))
#         if cur.fetchone():
#             return render_template('lab5/register.html', 
#                                    error="Такой пользователь уже существует")

#         # Хеширование пароля и добавление нового пользователя
#         password_hash = generate_password_hash(password)
#         insert_query = "INSERT INTO users (login, password) VALUES (%s, %s);" if current_app.config['DB_TYPE'] == 'postgres' else "INSERT INTO users (login, password) VALUES (?, ?);"
#         cur.execute(insert_query, (login, password_hash))

#     except Exception as e:
#         print(f"Ошибка выполнения SQL-запроса: {e}")
#         return render_template('lab5/register.html', 
#                                error="Произошла ошибка при регистрации")
#     finally:
#         db_close(conn, cur)

#     # Успешная регистрация
#     return render_template('lab5/success.html', login=login)

# @lab5.route('/lab5/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('lab5/login.html')
    
#     login = request.form.get('login')
#     password = request.form.get('password')

#     if not (login or password):
#         return render_template('lab5/login.html', error="Заполните поля")
    
#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Поиск пользователя в базе данных
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
#     else:
#         cur.execute("SELECT * FROM users WHERE login=?;", (login,))
#     user = cur.fetchone()

#     if not user or not check_password_hash(user['password'], password):
#         db_close(conn, cur)
#         return render_template('lab5/login.html', 
#                                error="Логин и/или пароль неверны")

#     # Сохранение логина пользователя в сессии
#     session['login'] = login 
#     db_close(conn, cur)
 
#     return render_template('lab5/success_login.html', login=login)

# @lab5.route('/lab5/create', methods=['GET', 'POST'])
# def create():
#     login = session.get('login')
#     if not login:
#         return redirect('/lab5/lab5/login')
    
#     if request.method == 'GET':
#         return render_template('lab5/create_article.html')
    
#     title = request.form.get('title')
#     article_text = request.form.get('article_text')

#     # Проверка на пустые поля
#     if not title or not article_text:
#         return render_template('lab5/create_article.html', error="Название и текст статьи не должны быть пустыми")

#     conn, cur = db_connect()

#     # Получение ID пользователя
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
#     else:
#         cur.execute("SELECT id FROM users WHERE login=?;", (login,))
#     login_id = cur.fetchone()["id"]

#     # Вставка статьи в базу данных
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);", (login_id, title, article_text))
#     else:
#         cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);", (login_id, title, article_text))

#     db_close(conn, cur)
#     return redirect('/lab5/lab5')

# @lab5.route('/lab5/list')
# def list():
#     login = session.get('login')
#     if not login:
#         return redirect('/lab5/lab5/login')

#     conn, cur = db_connect()

#     # Получение ID пользователя
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
#     else:
#         cur.execute("SELECT id FROM users WHERE login=?;", (login,))
#     login_id = cur.fetchone()["id"]

#     # Получение статей пользователя с любимыми статьями первыми
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC;", (login_id,))
#     else:
#         cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC;", (login_id,))
#     articles = cur.fetchall()

#     db_close(conn, cur)

#     # Проверка на отсутствие статей
#     if not articles:
#         message = "У вас пока нет статей."
#     else:
#         message = None

#     return render_template('/lab5/articles.html', articles=articles, message=message)

# @lab5.route('/lab5/logout')
# def logout():
#     session.pop('login', None)
#     return redirect('/lab5/lab5')

# @lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
# def edit(article_id):
#     login = session.get('login')
#     if not login:
#         return redirect('/lab5/lab5/login')

#     conn, cur = db_connect()

#     if request.method == 'GET':
#         # Получение статьи для редактирования
#         if current_app.config['DB_TYPE'] == 'postgres':
#             cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
#         else:
#             cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
#         article = cur.fetchone()
#         db_close(conn, cur)

#         if not article:
#             return redirect('/lab5/lab5/list')

#         return render_template('lab5/edit_article.html', article=article)
    
#     # Обновление статьи
#     title = request.form.get('title')
#     article_text = request.form.get('article_text')

#     if not title or not article_text:
#         return render_template('lab5/edit_article.html', article={'id': article_id, 'title': title, 'article_text': article_text}, error="Название и текст статьи не должны быть пустыми")

#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
#     else:
#         cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

#     db_close(conn, cur)
#     return redirect('/lab5/lab5/list')

# @lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
# def delete(article_id):
#     login = session.get('login')
#     if not login:
#         return redirect('/lab5/lab5/login')

#     conn, cur = db_connect()

#     # Удаление статьи
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
#     else:
#         cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

#     db_close(conn, cur)
#     return redirect('/lab5/lab5/list')

# @lab5.route('/lab5/users')
# def users():
#     login = session.get('login')
#     if not login:
#         return redirect('/lab5/lab5/login')
    
#     conn, cur = db_connect()

#     # Получение всех логинов пользователей
#     cur.execute("SELECT login FROM users;")
#     users = cur.fetchall()

#     db_close(conn, cur)
#     return render_template('lab5/users.html', users=users)

# @lab5.route('/lab5/public_articles')
# def public_articles():
#     conn, cur = db_connect()

#     # Получение всех публичных статей
#     cur.execute("SELECT articles.title, articles.article_text, users.login FROM articles JOIN users ON articles.login_id = users.id WHERE articles.is_public = TRUE;")
#     articles = cur.fetchall()

#     db_close(conn, cur)
#     return render_template('lab5/public_articles.html', articles=articles)