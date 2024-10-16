from flask import Blueprint, render_template, request, make_response, redirect, url_for

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

@lab3.route('/lab3/form1', methods=['GET'])
def form1():
    user = request.args.get('user') or ''
    age = request.args.get('age') or ''
    sex = request.args.get('sex') or ''

    errors = {}
    if not user:
        errors['user'] = 'Заполните поле!'

    sex_ru = 'Не указан'
    if sex == 'male':
        sex_ru = 'Мужской'
    elif sex == 'female':
        sex_ru = 'Женский'

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, sex_ru=sex_ru, errors=errors)

@lab3.route('/lab3/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        drink = request.form.get('drink')
        milk = 'milk' in request.form
        sugar = 'sugar' in request.form

        price = 0
        if drink == 'coffee':
            price = 120
        elif drink == 'black-tea':
            price = 80
        elif drink == 'green-tea':
            price = 70

        if milk:
            price += 30
        if sugar:
            price += 10

        return render_template('lab3/pay.html', price=price)

    return render_template('lab3/order.html')

@lab3.route('/lab3/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        card_number = request.form.get('card')
        card_name = request.form.get('name')
        card_cvv = request.form.get('cvv')

        # Здесь можно добавить логику проверки данных карты

        return render_template('lab3/success.html', price=request.form.get('price'))

    price = request.args.get('price')
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')

    if request.method == 'POST':
        new_color = request.form.get('color')
        new_background_color = request.form.get('background_color')
        new_font_size = request.form.get('font_size')

        response = make_response(redirect(url_for('lab3.settings')))
        if new_color:
            response.set_cookie('color', new_color)
        if new_background_color:
            response.set_cookie('background_color', new_background_color)
        if new_font_size:
            response.set_cookie('font_size', new_font_size + 'px')  # Добавляем 'px' к значению размера шрифта

        return response

    return render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size)