from flask import Blueprint, render_template, request

# Создание Blueprint
lab4 = Blueprint('lab4', __name__)

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
