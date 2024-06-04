
from flask import Flask
from flask import url_for
from flask import render_template
from markupsafe import escape

name = "Qingw"
movies = [
        {'title': 'My neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Socity', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'Wall-E', 'year': '2000'},
        {'title': 'The Pork of Music', 'year': '2012'}
]

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', name=name, movies=movies)
@app.route('/user/<name>')
def user_page(name):
    return f'User:{escape(name)}'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='qing'))
    print(url_for('user_page', name='w500'))
    print(url_for('test_url_for', num=2))

    return "Test_Page"
