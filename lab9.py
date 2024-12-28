from flask import Flask, Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__, template_folder='templates')

@lab9.route('/lab9/')
def index():
    return render_template('lab9/index.html')

@lab9.route('/lab9/step1_name', methods=['GET', 'POST'])
def step1_name():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        return redirect(url_for('lab9.step2_age'))
    return render_template('lab9/step1_name.html')

@lab9.route('/lab9/step2_age', methods=['GET', 'POST'])
def step2_age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect(url_for('lab9.step3_gender'))
    return render_template('lab9/step2_age.html')

@lab9.route('/lab9/step3_gender', methods=['GET', 'POST'])
def step3_gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect(url_for('lab9.step4_preference1'))
    return render_template('lab9/step3_gender.html')

@lab9.route('/lab9/step4_preference1', methods=['GET', 'POST'])
def step4_preference1():
    if request.method == 'POST':
        session['preference1'] = request.form.get('preference1')
        return redirect(url_for('lab9.step5_preference2'))
    return render_template('lab9/step4_preference1.html')

@lab9.route('/lab9/step5_preference2', methods=['GET', 'POST'])
def step5_preference2():
    if request.method == 'POST':
        session['preference2'] = request.form.get('preference2')
        return redirect(url_for('lab9.final'))
    return render_template('lab9/step5_preference2.html')

@lab9.route('/lab9/final')
def final():
    name = session.get('name', 'гость')
    age = int(session.get('age', 0))
    gender = session.get('gender')
    preference1 = session.get('preference1')
    preference2 = session.get('preference2')

    # Логика для формирования поздравления
    if age < 15:
        if gender == 'male':
            grown = 'Желаем, чтобы ты быстро вырос, был умным, счастливым и здоровым!'
        else:
            grown = 'Желаем, чтобы ты быстро выросла, была умной, счастливой и здоровой!'
    else:
        if gender == 'male':
            grown = 'Желаем успехов в новом году!'
        else:
            grown = 'Желаем счастья и здоровья в новом году!'

    if preference1 == 'вкусное' and preference2 == 'сладкое':
        gift = 'конфеты'
        img = 'candy.jpg'
    elif preference1 == 'вкусное' and preference2 == 'сытное':
        gift = 'пицца'
        img = 'pizza.jpg'
    else:
        gift = 'книга'
        img = 'book.png'

    return render_template('lab9/final.html', name=name, grown=grown, gift=gift, img=img)

@lab9.route('/lab9/restart')
def restart():
    session.clear()
    return redirect(url_for('lab9.step1_name'))