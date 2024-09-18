from flask import Flask, url_for, redirect

app=Flask(__name__)

@app.route("/")
@app.route("/web")
def start():
    return   """<!doctype html> 
    <html> 
       <body> 
           <h1>web-сервер на flask</h1> 
       </body> 
    </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@app.route("/author")
def author():
    name = "Афанасов Геракл Георгиевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''" alt="Дуб">
    </body>
</html>    
'''

count = 0

@app.route("/lab1/counter")
def counter():
    global count  
    count += 1
    return '''
<!doctype html> 
<html>
    <body>
        Сколько раз вы сюда заходили:  ''' + str(count) + '''
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то созданно ...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404




if __name__ == "__main__":
    app.run(debug=True)