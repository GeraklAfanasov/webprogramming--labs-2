from flask import Blueprint, render_template, request, redirect, url_for, flash
import re

lab4 = Blueprint('lab4', __name__)

# Главная страница для lab4
@lab4.route('/lab4/')
def lab4_main():
    return render_template('lab4/lab4_main.html')

# Страница для калькулятора
@lab4.route('/lab4/div-form', methods=['GET', 'POST'])
def div_form():
    error = None
    result = None
    num1 = None
    num2 = None

    if request.method == 'POST':
        try:
            num1 = request.form.get('x1').replace(',', '.')
            num2 = request.form.get('x2').replace(',', '.')

            # Проверяем, что введены только цифры или десятичные точки
            if not (re.match(r'^\d*\.?\d*$', num1) and re.match(r'^\d*\.?\d*$', num2)):
                raise ValueError("Пожалуйста, вводите только цифры.")

            num1, num2 = float(num1), float(num2)

            if num2 == 0:
                raise ValueError("Деление на ноль невозможно.")

            result = num1 / num2
        except ValueError as e:
            error = str(e)

    return render_template('lab4/div_form.html', error=error, result=result, x1=num1, x2=num2)

