# WEB SERVER to run the Catalog App using Flask

# Import modules for Flask and Sqlalchemy needed to run the webserver
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book_genres, Books, User

# Import modules for registration and authentication
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json','r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Connect to Database bookstore.db and create database session
engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User Helper Functions

# create a user in the bookstore.db
def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session[
				'email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

# Helper function to obtain the user object based on user_id
def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user

# Helper function to get user id based on email
def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

# Following are 8 functionalities supported by the web server
# 1. show all genres
# Depending on whether user has logged in or not
# public or private page is shown
@app.route('/')
@app.route('/genres/')
def getBookGenres():
	genres = session.query(Book_genres).all()
	if 'username' not in login_session:
		return render_template('PublicBookStore.html',genres=genres)
	else:
		return render_template('BookStore.html',genres=genres)

# 2. create a new genre
# If the method is GET, render a form to fill in
# If the method is POST, check that the Genre does not already exist
# If the genre is a new one and user exists in database, create a new genre
# and take user back to the homepage.
# In failure cases too, take the user back to homepage
@app.route('/genres/new', methods=['GET', 'POST'])
def createNewGenre():
	if 'username' not in login_session:
		return redirect('login')

	if request.method == 'POST':
		print request.form['name']
		new_genre_name = request.form['name']
		allGenres = getAllGenresInDatabase()
		result = [i for i in allGenres if new_genre_name in allGenres]
		print result

		userid = getUserID(login_session['email'])
		print userid
		if userid != None:
			if not result:
				new_book_genre = Book_genres(name=new_genre_name, user_id=userid)
				session.add(new_book_genre)
				session.commit()
				flash("New Genre created!!")
				return redirect(url_for('getBookGenres'))
			else:
				print 'Genre already exists'
				flash("Provided genre already exists")
				return redirect(url_for('getBookGenres'))
		else:
			flash("user's id not found")
			return redirect(url_for('getBookGenres'))
	else:
		return render_template('NewGenre.html')


# Helper function to obtain all genres in the database currently
# It is used to check if a genre already exists or not when creating a new one
def getAllGenresInDatabase():
	genres = session.query(Book_genres).all()
	aList = []

	for i in genres:
		aList.append(i.name)
	print aList
	return aList

# 3. List books of a genre
# If the user is not logged in or user's id does not match the creator's id
# Just show a public page where no edit or delete button is shown
# Otherwise, show a private page
@app.route('/genres/<int:genre_id>/')
@app.route('/genres/<int:genre_id>/list')
def displayGenre(genre_id):
	genre = session.query(Book_genres).filter_by(id=genre_id).one()
	creator = getUserInfo(genre.user_id)
	books = session.query(Books).filter_by(book_genre_id=genre_id).all()
	#print login_session
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('PublicList_Books.html',genre_title=genre.name,genre_id=genre_id,books=books,creator_name=creator.name)
	else:
		return render_template('List_Books.html',genre_title=genre.name,genre_id=genre_id,books=books)

# 4. Edit a genre
# If user has not logged in, redirect user to login page
# If user has logged in but not the genre's creator, the user cannot edit that genre
# Otherwise, If the method is GET, render the form page to fill out
# If the method is POST, update the fields that are modified
# and take the user to home page
@app.route('/genres/<int:genre_id>/edit', methods=['GET','POST'])
def editGenre(genre_id):
	if 'username' not in login_session:
		return redirect('login')
	genreQuery = session.query(Book_genres).filter_by(id=genre_id).one()
	if genreQuery.user_id != login_session['user_id']:
		return "<script> function myFunction() {alert('You are not authorized to perfrom this function.You are not creator of this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		print request.form['name']
		edited_genre_name = request.form['name']
		genreQuery.name = edited_genre_name
		session.add(genreQuery)
		session.commit()
		flash("Genre name edited!!")
		return redirect(url_for('getBookGenres'))
	else:
		return render_template('EditGenre.html',genre_id=genre_id, genre_name=genreQuery.name)


# 5. Delete a genre
# If user has not logged in, redirect user to login page
# If user has logged in but not the genre's creator, the user cannot delete that genre
# Otherwise, If the method is GET, render the form page to provide confirmation for deletion
# If the method is POST, delete the genre and take the user to home page
@app.route('/genres/<int:genre_id>/delete', methods=['GET','POST'])
def deleteGenre(genre_id):
	if 'username' not in login_session:
		return redirect('login')
	genreQuery = session.query(Book_genres).filter_by(id=genre_id).one()
	if genreQuery.user_id != login_session['user_id']:
		return "<script> function myFunction() {alert('You are not authorized to perfrom this function.You are not creator of this item.');}</script><body onload='myFunction()''>"

	if request.method == 'POST':
		session.delete(genreQuery)
		session.commit()
		flash("Genre name removed!!")
		return redirect(url_for('getBookGenres'))
	else:
		return render_template('DeleteGenre.html',genre_id=genre_id, genre_name=genreQuery.name)


# 6. create a new book under a genre
# If user has not logged in, redirect user to login page
# If user has logged in but does not match the genre' creator, then user cannot add a book
# Otherwise, if the method is GET, render the form page to provide details about the book
# If the method is POST, create a new book under that genre and take user to the genre details page
@app.route('/genres/<int:genre_id>/list/new', methods=['GET', 'POST'])
def createNewBook(genre_id):
	if 'username' not in login_session:
		return redirect('login')
	genreQuery = session.query(Book_genres).filter_by(id=genre_id).one()
	if genreQuery.user_id != login_session['user_id']:
		return "<script> function myFunction() {alert('You are not authorized to perfrom this function.You are not creator of this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		new_book_genre = Books(name=request.form['book_title'],
								description=request.form['description'],
								author=request.form['author'],
								price=request.form['price'],
								user_id=genreQuery.user_id,
								book_genre=genreQuery)
		session.add(new_book_genre)
		session.commit()
		flash("New Book to genre!!")
		return redirect(url_for('displayGenre',genre_id=genre_id))
	else:
		return render_template('NewBook.html',genre_id=genre_id,genre_name=genreQuery.name)


# 7. Edit a book under a genre
# If user has not logged in, redirect user to login page
# If user has logged in but does not match the genre's creator, the operation is not permitted
# Otherwise, if method is GET, render a form to provide the information
# If the method is POST, update the details (not all fields may not be changed)
# and user will be taken to the genre details page
@app.route('/genres/<int:genre_id>/list/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(genre_id,book_id):
	if 'username' not in login_session:
		return redirect('login')
	bookQuery = session.query(Books).filter_by(book_genre_id=genre_id).filter_by(id=book_id).one()
	if bookQuery.user_id != login_session['user_id']:
		return "<script> function myFunction() {alert('You are not authorized to perfrom this function.You are not creator of this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['book_title']:
			bookQuery.name= request.form['book_title']
		if request.form['description']:
			bookQuery.description=request.form['description']
		if request.form['author']:
			bookQuery.author=request.form['author']
		if request.form['price']:
			bookQuery.price=request.form['price']
		session.add(bookQuery)
		session.commit()
		flash("Edited the book in the selected genre!!")
		return redirect(url_for('displayGenre',genre_id=genre_id))
	else:
		return render_template('EditBook.html',genre_id=genre_id,book_title=bookQuery.name,book_id=book_id)

# 8. Delete a book under a genre
# If user has not logged in, redirect user to login page
# If user has logged in but does not match the genre's creator, the operation is not permitted
# Otherwise, if method is GET, render a form to provide the confirmation
# If the method is POST, delete the book
# and user will be taken to the genre details page
@app.route('/genres/<int:genre_id>/list/<int:book_id>/delete', methods=['GET','POST'])
def deleteBook(genre_id,book_id):
	if 'username' not in login_session:
		return redirect('login')
	bookQuery = session.query(Books).filter_by(book_genre_id=genre_id).filter_by(id=book_id).one()
	if bookQuery.user_id != login_session['user_id']:
		return "<script> function myFunction() {alert('You are not authorized to perfrom this function.You are not creator of this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(bookQuery)
		session.commit()
		flash("Book removed!!")
		return redirect(url_for('displayGenre',genre_id=genre_id))
	else:
		return render_template('DeleteBook.html',genre_id=genre_id, book_title=bookQuery.name,book_id=book_id)

# Json endpoint to get all books of a genre
@app.route('/genres/<int:genre_id>/list/JSON')
def bookListJSON(genre_id):
	genre = session.query(Book_genres).filter_by(id=genre_id).one()
	items = session.query(Books).filter_by(
		book_genre_id=genre_id).all()
	return jsonify(Books=[i.serialize for i in items])

# Json endpoint to get all books of a genre
@app.route('/genres/<int:genre_id>/list/<int:book_id>/JSON')
def bookJSON(genre_id,book_id):
	genre = session.query(Book_genres).filter_by(id=genre_id).one()
	items = session.query(Books).filter_by(
		book_genre_id=genre_id).filter_by(id=book_id).all()
	return jsonify(Books=[i.serialize for i in items])

# Json endpoint to get all genres
@app.route('/genres/JSON')
def genreListJSON():
	genreQuery = session.query(Book_genres).all()
	return jsonify(Book_genres=[i.serialize for i in genreQuery])

# Create login page
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	#return "The current session state is %s" % login_session['state']
	return render_template('login.html', STATE=state)

# CONNECT - obtain google plus authentication credentials
@app.route('/gconnect', methods=['POST'])
def gconnect():
	print login_session['state']
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		% access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	print login_session['username']
	print login_session['email']
	print login_session['gplus_id']

	user_id = getUserID(data['email'])
	if user_id is None:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1 style="text-align: center; color: #ffffff;" >Welcome, '
	output += login_session['username']
	output += '!</h1>'
	#output += '<img src="'
	#output += login_session['picture']
	#output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(
		json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# Reset the user's sesson.
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		# For whatever reason, the given token was invalid.
		response = make_response(
			json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)