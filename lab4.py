from flask import Blueprint, render_template, request, redirect, url_for, session

# Создание Blueprint
lab4 = Blueprint('lab4', __name__)

tree_count = 0

@lab4.route('/lab4/')
def lab4_main():
    return render_template('lab4/lab4_main.html')

@lab4.route('/sum', methods=['GET', 'POST'])
def sum_page():
    if request.method == 'POST':
        num1 = request.form.get('num1', default=0, type=float)
        num2 = request.form.get('num2', default=0, type=float)
        result = num1 + num2
        return render_template('lab4/sum.html', result=result)
    return render_template('lab4/sum.html', result=None)

@lab4.route('/subtract', methods=['GET', 'POST'])
def subtract_page():
    error = None
    result = None
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        if num1 == '' or num2 == '':
            error = "Оба поля должны быть заполнены."
        else:
            result = float(num1) - float(num2)
    return render_template('lab4/subtract.html', error=error, result=result)

@lab4.route('/multiply', methods=['GET', 'POST'])
def multiply_page():
    if request.method == 'POST':
        num1 = request.form.get('num1', default=1, type=float)
        num2 = request.form.get('num2', default=1, type=float)
        result = num1 * num2
        return render_template('lab4/multiply.html', result=result)
    return render_template('lab4/multiply.html', result=None)

@lab4.route('/power', methods=['GET', 'POST'])
def power_page():
    error = None
    result = None
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        if num1 == '' or num2 == '':
            error = "Оба поля должны быть заполнены."
        elif float(num1) == 0 and float(num2) == 0:
            error = "Нельзя возводить 0 в 0."
        else:
            result = float(num1) ** float(num2)
    return render_template('lab4/power.html', error=error, result=result)

@lab4.route('/div', methods=['GET', 'POST'])
def div_page():
    error = None
    result = None
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        if num1 == '' or num2 == '':
            error = "Оба поля должны быть заполнены."
        elif float(num2) == 0:
            error = "Деление на ноль невозможно."
        else:
            result = float(num1) / float(num2)
    return render_template('lab4/div.html', error=error, result=result)

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'plant':
            tree_count += 1
        elif operation == 'cut':
            if tree_count > 0:
                tree_count -= 1
        return redirect(url_for('lab4.tree'))

    return render_template('lab4/tree.html', tree_count=tree_count)

# Роут для страницы авторизации
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    error = None
    authorized = False
    
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        print(f"Login: {login}, Password: {password}")  # Отладочная печать
        
        if login == 'alex' and password == '123':
            session['authorized'] = True
            authorized = True
        else:
            error = "Неверные логин или пароль."
    else:
        # Проверяем авторизован ли пользователь
        authorized = session.get('authorized', False)
    
    return render_template('lab4/login.html', error=error, authorized=authorized)