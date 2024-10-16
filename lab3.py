from flask import Blueprint, render_template, make_response, redirect, url_for, request
import time

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab3_main():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

@lab3.route('/lab3/cookie/', methods=['GET', 'POST'])
def set_cookie():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        name_color = request.form.get('name_color')

        response = make_response(redirect(url_for('lab3.lab3_main')))
        response.set_cookie('name', name, max_age=5)  # Куки будут жить 5 секунд
        response.set_cookie('age', age)
        response.set_cookie('name_color', name_color)
        return response

    return '''
        <form method="post">
            <label for="name">Имя:</label>
            <input type="text" id="name" name="name" required>
            <br>
            <label for="age">Возраст:</label>
            <input type="text" id="age" name="age" required>
            <br>
            <label for="name_color">Цвет текста:</label>
            <input type="text" id="name_color" name="name_color" required>
            <br>
            <button type="submit">Установить куки</button>
        </form>
    '''

@lab3.route('/lab3/clear_cookies/')
def clear_cookies():
    response = make_response(redirect(url_for('lab3.lab3_main')))
    response.delete_cookie('name')
    response.delete_cookie('age')
    response.delete_cookie('name_color')
    return response