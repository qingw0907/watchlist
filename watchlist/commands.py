import click
from watchlist import app, db
from watchlist.models import User, Movie


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login!')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
	db.create_all()
	user = User.query.first()
	if user is not None:
		click.echo('Updating user...')
		user.username = username
		user.set_password(password)
	else:
		click.echo('Creating user...')
		user = User(username=username, name='Admin')
		user.set_password(password)
		db.session.add(user)

	db.session.commit()
	click.echo('Done')
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
	click.echo('Done.')

