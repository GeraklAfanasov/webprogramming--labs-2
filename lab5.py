from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Gerakl'  # Необходимо для работы сессий

# Подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname='gerakl_afanasov_knowledge_base',
        user='postgres',
        password='Gerakl2288',
        host='localhost'
    )
    return conn

# Закрытие подключения к базе данных и выполнение commit
def close_db_connection(conn, cur):
    cur.close()
    conn.commit()
    conn.close()

# Создание Blueprint
lab5 = Blueprint('lab5', __name__)

# Маршруты и логика приложения
@lab5.route('/lab5/')
def lab():
    """Главная страница лабораторной"""
    return render_template('lab5/lab5.html', login=session.get('login', 'anonymous'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE login = %s", (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['username'] = username
            close_db_connection(conn, cur)
            return redirect(url_for('lab5.create_article'))

        close_db_connection(conn, cur)
        flash('Неправильный логин или пароль')
    
    return render_template('lab5/login.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (username, hashed_password))
        close_db_connection(conn, cur)
        
        flash('Пользователь успешно зарегистрирован!')
        return redirect(url_for('lab5.login'))
    
    return render_template('lab5/register.html')

@lab5.route('/lab5/list_articles')
def list_articles():
    """Страница со списком статей"""
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для просмотра статей.')
        return redirect(url_for('lab5.login'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    close_db_connection(conn, cur)
    
    return render_template('lab5/list.html', articles=articles)

@lab5.route('/lab5/create_article', methods=['GET', 'POST'])
def create_article():
    """Страница создания статьи"""
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для создания статьи.')
        return redirect(url_for('lab5.login'))
    
    if request.method == 'POST':
        title = request.form['title']
        article_text = request.form['article_text']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE login = %s", (session['username'],))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
        close_db_connection(conn, cur)
        
        return redirect(url_for('lab5.list_articles'))
    
    return render_template('lab5/create.html')

@lab5.route('/lab5/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    """Страница редактирования статьи"""
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для редактирования статьи.')
        return redirect(url_for('lab5.login'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cur.fetchone()
    
    if not article:
        close_db_connection(conn, cur)
        return "Статья не найдена", 404

    if request.method == 'POST':
        title = request.form['title']
        article_text = request.form['article_text']
        
        cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s", (title, article_text, article_id))
        close_db_connection(conn, cur)
        
        return redirect(url_for('lab5.list_articles'))

    close_db_connection(conn, cur)
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    """Удаление статьи"""
    if 'username' not in session:
        flash('Пожалуйста, войдите в систему для удаления статьи.')
        return redirect(url_for('lab5.login'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    close_db_connection(conn, cur)
    
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/logout')
def logout():
    """Выход из системы"""
    session.pop('username', None)
    return redirect(url_for('lab5.lab'))

# Регистрация Blueprint
app.register_blueprint(lab5)

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
# import psycopg2
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'Gerakl'  # Необходимо для работы сессий

# # Подключение к базе данных
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname='gerakl_afanasov_knowledge_base',
#         user='postgres',
#         password='Gerakl2288',
#         host='localhost'
#     )
#     return conn

# # Закрытие подключения к базе данных и выполнение commit
# def close_db_connection(conn, cur):
#     cur.close()
#     conn.commit()
#     conn.close()

# # Создание Blueprint
# lab5 = Blueprint('lab5', __name__)

# # Маршруты и логика приложения
# @lab5.route('/lab5/')
# def lab():
#     """Главная страница лабораторной"""
#     return render_template('lab5/lab5.html', login=session.get('login', 'anonymous'))

# @lab5.route('/lab5/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users WHERE login = %s", (username,))
#         user = cur.fetchone()
        
#         if user and check_password_hash(user[2], password):
#             session['username'] = username
#             close_db_connection(conn, cur)
#             return redirect(url_for('lab5.create_article'))

#         close_db_connection(conn, cur)
#         flash('Неправильный логин или пароль')
    
#     return render_template('lab5/login.html')

# @lab5.route('/lab5/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         username = request.form['username']
#         password = request.form['password']
        
#         hashed_password = generate_password_hash(password)
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (username, hashed_password))
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
        
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT id FROM users WHERE login = %s", (session['username'],))
#         user_id = cur.fetchone()[0]
#         cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
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
#     cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
#     article = cur.fetchone()
    
#     if not article:
#         close_db_connection(conn, cur)
#         return "Статья не найдена", 404

#     if request.method == 'POST':
#         title = request.form['title']
#         article_text = request.form['article_text']
        
#         cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s", (title, article_text, article_id))
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
#     cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
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