import os
from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Установка конфигурации
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'Gerakl')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')  # По умолчанию используем SQLite

def get_db_connection():
    db_type = current_app.config.get('DB_TYPE', 'sqlite')
    if db_type == 'postgres':
        conn = connect(
            host='127.0.0.1',
            database='gerakl_afanasov_knowledge_base',
            user='postgres',
            password='Gerakl2288',
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
    else:
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def close_db_connection(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.commit()
        conn.close()

# Создание Blueprint
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('username', 'anonymous'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Логин и пароль не могут быть пустыми')
            return render_template('lab5/login.html')
        conn, cur = get_db_connection()
        cur.execute("SELECT * FROM users WHERE login = ?", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            close_db_connection(conn, cur)
            return redirect(url_for('lab5.create_article'))
        close_db_connection(conn, cur)
        flash('Неправильный логин или пароль')
    return render_template('lab5/login.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Логин и пароль не могут быть пустыми')
            return render_template('lab5/register.html')
        conn, cur = get_db_connection()
        cur.execute("SELECT * FROM users WHERE login = ?", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            close_db_connection(conn, cur)
            flash('Логин уже занят')
            return render_template('lab5/register.html')
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (username, hashed_password))
        close_db_connection(conn, cur)
        flash('Пользователь успешно зарегистрирован!')
        return redirect(url_for('lab5.login'))
    return render_template('lab5/register.html')

@lab5.route('/lab5/list_articles')
def list_articles():
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для просмотра статей.')
        return redirect(url_for('lab5.login'))
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    close_db_connection(conn, cur)
    return render_template('lab5/list.html', articles=articles)

@lab5.route('/lab5/create_article', methods=['GET', 'POST'])
def create_article():
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для создания статьи.')
        return redirect(url_for('lab5.login'))
    if request.method == 'POST':
        title = request.form['title']
        article_text = request.form['article_text']
        if not title or not article_text:
            flash('Заголовок и текст статьи не могут быть пустыми')
            return render_template('lab5/create.html')
        conn, cur = get_db_connection()
        cur.execute("SELECT id FROM users WHERE login = ?", (session['username'],))
        user_id = cur.fetchone()['id']
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?)", (user_id, title, article_text))
        close_db_connection(conn, cur)
        return redirect(url_for('lab5.list_articles'))
    return render_template('lab5/create.html')

@lab5.route('/lab5/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для редактирования статьи.')
        return redirect(url_for('lab5.login'))
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    article = cur.fetchone()
    if not article:
        close_db_connection(conn, cur)
        return "Статья не найдена", 404
    if request.method == 'POST':
        title = request.form['title']
        article_text = request.form['article_text']
        cur.execute("UPDATE articles SET title = ?, article_text = ? WHERE id = ?", (title, article_text, article_id))
        close_db_connection(conn, cur)
        return redirect(url_for('lab5.list_articles'))
    close_db_connection(conn, cur)
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для удаления статьи.')
        return redirect(url_for('lab5.login'))
    conn, cur = get_db_connection()
    cur.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    close_db_connection(conn, cur)
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('lab5.lab'))

app.register_blueprint(lab5)

if __name__ == '__main__':
    app.run(debug=True)


# import os
# from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash, current_app
# from werkzeug.security import generate_password_hash, check_password_hash
# import sqlite3
# from pathlib import Path
# import sqlite3
# from os import path
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = Flask(__name__)

# def get_db_connection():
#     if current_app.config['DB_TYPE'] == 'postgres':
#         conn = psycopg2.connect(
#             host='127.0.0.1',
#             database='gerakl_afanasov_knowledge_base',
#             user='postgres',
#             password='Gerakl2288'
#         )
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#     else:
#         dir_path = path.dirname(path.realpath(__file__))
#         db_path = path.join(dir_path, 'database.db')
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()

#     return conn, cur

# def close_db_connection(conn, cur):
#     if conn and cur:
#         conn.commit()
#         cur.close()
#         conn.close()

# # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'секретно-секрflask runетный-секрет')
# # app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

# # # Подключение к базе данных
# # def get_db_connection():
# #     db_type = current_app.config['DB_TYPE']
# #     if db_type == 'postgres':
# #         db_path = Path(current_app.root_path) / 'database.db'
# #         conn = sqlite3.connect(db_path)
# #         conn.row_factory = sqlite3.Row  # Возвращает результаты в виде словаря
# #         return conn
# #     else:
# #         raise ValueError(f"Unsupported DB_TYPE: {db_type}")

# # # Закрытие подключения к базе данных и выполнение commit
# # def close_db_connection(conn, cur):
# #     cur.close()
# #     conn.commit()
# #     conn.close()

# # Создание Blueprint
# lab5 = Blueprint('lab5', __name__)

# # Маршруты и логика приложения
# @lab5.route('/lab5/')
# def lab():
#     """Главная страница лабораторной"""
#     return render_template('lab5/lab5.html', login=session.get('username', 'anonymous'))

# @lab5.route('/lab5/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if not username or not password:
#             flash('Логин и пароль не могут быть пустыми')
#             return render_template('lab5/login.html')
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users WHERE login = ?", (username,))
#         user = cur.fetchone()
        
#         if user and check_password_hash(user['password'], password):
#             session['username'] = username
#             close_db_connection(conn, cur)
#             return redirect(url_for('lab5.create_article'))

#         close_db_connection(conn, cur)
#         flash('Неправильный логин или пароль')
    
#     return render_template('lab5/login.html')

# @lab5.route('/lab5/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if not username or not password:
#             flash('Логин и пароль не могут быть пустыми')
#             return render_template('lab5/register.html')
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users WHERE login = ?", (username,))
#         existing_user = cur.fetchone()
        
#         if existing_user:
#             close_db_connection(conn, cur)
#             flash('Логин уже занят')
#             return render_template('lab5/register.html')
        
#         hashed_password = generate_password_hash(password)
#         cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (username, hashed_password))
#         close_db_connection(conn, cur)
        
#         flash('Пользователь успешно зарегистрирован!')
#         return redirect(url_for('lab5.login'))
    
#     return render_template('lab5/register.html')

# @lab5.route('/lab5/list_articles')
# def list_articles():
#     """Страница со списком статей"""
#     if 'username' not in session:
#         flash('Пожалуйста, войдите в систему для просмотра статей.')
#         return redirect(url_for('lab5.login'))
    
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM articles")
#     articles = cur.fetchall()
#     close_db_connection(conn, cur)
    
#     return render_template('lab5/list.html', articles=articles)

# @lab5.route('/lab5/create_article', methods=['GET', 'POST'])
# def create_article():
#     """Страница создания статьи"""
#     if 'username' not in session:
#         flash('Пожалуйста, войдите в систему для создания статьи.')
#         return redirect(url_for('lab5.login'))
    
#     if request.method == 'POST':
#         title = request.form['title']
#         article_text = request.form['article_text']
        
#         if not title or not article_text:
#             flash('Заголовок и текст статьи не могут быть пустыми')
#             return render_template('lab5/create.html')
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT id FROM users WHERE login = ?", (session['username'],))
#         user_id = cur.fetchone()['id']
#         cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?)", (user_id, title, article_text))
#         close_db_connection(conn, cur)
        
#         return redirect(url_for('lab5.list_articles'))
    
#     return render_template('lab5/create.html')

# @lab5.route('/lab5/edit_article/<int:article_id>', methods=['GET', 'POST'])
# def edit_article(article_id):
#     """Страница редактирования статьи"""
#     if 'username' not in session:
#         flash('Пожалуйста, войдите в систему для редактирования статьи.')
#         return redirect(url_for('lab5.login'))
    
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
#     article = cur.fetchone()
    
#     if not article:
#         close_db_connection(conn, cur)
#         return "Статья не найдена", 404

#     if request.method == 'POST':
#         title = request.form['title']
#         article_text = request.form['article_text']
        
#         cur.execute("UPDATE articles SET title = ?, article_text = ? WHERE id = ?", (title, article_text, article_id))
#         close_db_connection(conn, cur)
        
#         return redirect(url_for('lab5.list_articles'))

#     close_db_connection(conn, cur)
#     return render_template('lab5/edit_article.html', article=article)

# @lab5.route('/lab5/delete_article/<int:article_id>', methods=['POST'])
# def delete_article(article_id):
#     """Удаление статьи"""
#     if 'username' not in session:
#         flash('Пожалуйста, войдите в систему для удаления статьи.')
#         return redirect(url_for('lab5.login'))
    
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM articles WHERE id = ?", (article_id,))
#     close_db_connection(conn, cur)
    
#     return redirect(url_for('lab5.list_articles'))

# @lab5.route('/lab5/logout')
# def logout():
#     """Выход из системы"""
#     session.pop('username', None)
#     return redirect(url_for('lab5.lab'))

# # Регистрация Blueprint
# app.register_blueprint(lab5)

# if __name__ == '__main__':
#     app.run(debug=True)




# # from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
# # import psycopg2
# # from werkzeug.security import generate_password_hash, check_password_hash

# # app = Flask(__name__)
# # app.secret_key = 'Gerakl'  # Необходимо для работы сессий

# # # Подключение к базе данных
# # def get_db_connection():
# #     conn = psycopg2.connect(
# #         dbname='gerakl_afanasov_knowledge_base',
# #         user='postgres',
# #         password='Gerakl2288',
# #         host='localhost'
# #     )
# #     return conn

# # # Закрытие подключения к базе данных и выполнение commit
# # def close_db_connection(conn, cur):
# #     cur.close()
# #     conn.commit()
# #     conn.close()

# # # Создание Blueprint
# # lab5 = Blueprint('lab5', __name__)

# # # Маршруты и логика приложения
# # @lab5.route('/lab5/')
# # def lab():
# #     """Главная страница лабораторной"""
# #     return render_template('lab5/lab5.html', login=session.get('login', 'anonymous'))

# # @lab5.route('/lab5/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
        
# #         if not username or not password:
# #             flash('Логин и пароль не могут быть пустыми')
# #             return render_template('lab5/login.html')
        
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute("SELECT * FROM users WHERE login = %s", (username,))
# #         user = cur.fetchone()
        
# #         if user and check_password_hash(user[2], password):
# #             session['username'] = username
# #             close_db_connection(conn, cur)
# #             return redirect(url_for('lab5.create_article'))

# #         close_db_connection(conn, cur)
# #         flash('Неправильный логин или пароль')
    
# #     return render_template('lab5/login.html')

# # @lab5.route('/lab5/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         name = request.form['name']
# #         username = request.form['username']
# #         password = request.form['password']
        
# #         if not username or not password:
# #             flash('Логин и пароль не могут быть пустыми')
# #             return render_template('lab5/register.html')
        
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute("SELECT * FROM users WHERE login = %s", (username,))
# #         existing_user = cur.fetchone()
        
# #         if existing_user:
# #             close_db_connection(conn, cur)
# #             flash('Логин уже занят')
# #             return render_template('lab5/register.html')
        
# #         hashed_password = generate_password_hash(password)
# #         cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (username, hashed_password))
# #         close_db_connection(conn, cur)
        
# #         flash('Пользователь успешно зарегистрирован!')
# #         return redirect(url_for('lab5.login'))
    
# #     return render_template('lab5/register.html')

# # @lab5.route('/lab5/list_articles')
# # def list_articles():
# #     """Страница со списком статей"""
# #     if 'username' not in session:
# #         flash('Пожалуйста, войдите в систему для просмотра статей.')
# #         return redirect(url_for('lab5.login'))
    
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT * FROM articles")
# #     articles = cur.fetchall()
# #     close_db_connection(conn, cur)
    
# #     return render_template('lab5/list.html', articles=articles)

# # @lab5.route('/lab5/create_article', methods=['GET', 'POST'])
# # def create_article():
# #     """Страница создания статьи"""
# #     if 'username' not in session:
# #         flash('Пожалуйста, войдите в систему для создания статьи.')
# #         return redirect(url_for('lab5.login'))
    
# #     if request.method == 'POST':
# #         title = request.form['title']
# #         article_text = request.form['article_text']
        
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute("SELECT id FROM users WHERE login = %s", (session['username'],))
# #         user_id = cur.fetchone()[0]
# #         cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
# #         close_db_connection(conn, cur)
        
# #         return redirect(url_for('lab5.list_articles'))
    
# #     return render_template('lab5/create.html')

# # @lab5.route('/lab5/edit_article/<int:article_id>', methods=['GET', 'POST'])
# # def edit_article(article_id):
# #     """Страница редактирования статьи"""
# #     if 'username' not in session:
# #         flash('Пожалуйста, войдите в систему для редактирования статьи.')
# #         return redirect(url_for('lab5.login'))
    
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
# #     article = cur.fetchone()
    
# #     if not article:
# #         close_db_connection(conn, cur)
# #         return "Статья не найдена", 404

# #     if request.method == 'POST':
# #         title = request.form['title']
# #         article_text = request.form['article_text']
        
# #         cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s", (title, article_text, article_id))
# #         close_db_connection(conn, cur)
        
# #         return redirect(url_for('lab5.list_articles'))

# #     close_db_connection(conn, cur)
# #     return render_template('lab5/edit_article.html', article=article)

# # @lab5.route('/lab5/delete_article/<int:article_id>', methods=['POST'])
# # def delete_article(article_id):
# #     """Удаление статьи"""
# #     if 'username' not in session:
# #         flash('Пожалуйста, войдите в систему для удаления статьи.')
# #         return redirect(url_for('lab5.login'))
    
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
# #     close_db_connection(conn, cur)
    
# #     return redirect(url_for('lab5.list_articles'))

# # @lab5.route('/lab5/logout')
# # def logout():
# #     """Выход из системы"""
# #     session.pop('username', None)
# #     return redirect(url_for('lab5.lab'))

# # # Регистрация Blueprint
# # app.register_blueprint(lab5)

# # if __name__ == '__main__':
# #     app.run(debug=True)