from flask import Flask
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import os
import click
from flask import request, redirect, flash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path,'data.db')
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	year = db.Column(db.String(4))

@app.context_processor
def inject_user():
	user = User.query.first()
	return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	if drop:
		db.drop_all()
	db.create_all()
	click.echo('Initialized database')

@app.cli.command()
def forge():
	db.create_all()
	
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

	user = User(name=name)
	db.session.add(user)
	for m in movies:
		movie = Movie(title=m['title'], year=m['year'])
		db.session.add(movie)

	db.session.commit()
	click.echo('Done')


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		title = request.form.get('title')
		year = request.form.get('year')
		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('Invalid input.')
			return redirect(url_for('index'))
		movie = Movie(title=title, year=year)
		db.session.add(movie)
		db.session.commit()
		flash('Item created.')
		return redirect(url_for('index'))	
	movies = Movie.query.all()
	return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['POST', 'GET'])
def edit(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	if request.method == 'POST':
		title = request.form['title']
		year = request.form['year']
		if not title or not year or len(title) > 60 or len(year) > 4:
			flash('Invalid input.')
			redirect(url_for('edit', movie_id=movie_id))
		movie.year = year
		movie.title = title
		db.session.commit()
		flash('Item updated.')
		return redirect(url_for('index'))

	return render_template('edit.html', movie=movie)
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash("Item deleted")
	return redirect(url_for('index'))
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
