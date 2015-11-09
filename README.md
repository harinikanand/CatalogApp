Author: Harini

Date: 11/09/2015

Title: Catalog App

Description: The Catalog App project develops an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

I have developed the Catalog App for a book store called Awesome book store.

The home page shows all the categories (genres). There are two homepages - public home page and a private home page (for a user who has successfully logged in and registered)
The private page allows users to add a new genre, edit and delete genres.

Additionally clicking on each genre shows all the books (titles) under the genre.
Here also there are two pages - a public version (with no create, edit or delete options) and a private page
- where a user can perform edit and delete provided they are creators of the books.
There is also an option to create a new title for a book.

Prerequisies:
  - git, Vagrant terminal and a Virtual Box ( Follow instructions located here: https://www.udacity.com/wiki/ud088/vagrant )
  - open git bash terminal
  - install Flask
    pip install werkzeug==0.8.3
    pip install flask==0.9
    pip install Flask-Login==0.1.3


Steps to run the application:

0. Open a git bash terminal

1. git clone the catalog app

2. cd to CatalogApp folder

3. First create a database for the bookstore (it is called bookstore.db). This is done by running:
   python database_setup.py
   This will create bookstore.db in your folder

4. To have some data in the bookstore.db, run the file lotsofbooks.py
   python lotsofbooks.py

   It should show "added book genres!"

5. To run the web server, type:
   python finalproject.py
   This provides a address (http://localhost:5000)

6. Open a browser like google chrome and type the url (http://localhost:5000/login)

7. The following public URLs are supported;
        1. http://localhost:5000/login - provide a mechanism to login
        2. http://localhost:5000/ - same as the URL 7.3
        3. http://localhost:5000/genres - shows all the genres
        4. http://localhost:5000/genres/<int:genre_id>/ - same as 7.5
        5. http://localhost:5000/genres/<int:genre_id>/list - shows all the books in the genre with genre_id
        6. http://localhost:5000/genres/<int:genre_id>/list/JSON - Shows the JSON output for all the books in a genre with id genre_id
        7. http://localhost:5000/genres/<int:genre_id>/list/<int:book_id>/JSON - shows the JSON putput for all book with book_id in the genre genre_id.
         http://localhost:5000/genres/JSON - shows the JSON output for all the genres
8.  The following Private URLs are supported:
         http://localhost:5000/genres/new - URL to add a new genre
         http://localhost:5000/genres/<int:genre_id>/edit - URL for editing the genre with genre_id
         http://localhost:5000/genres/<int:genre_id>/delete - URL for deleting the genre with genre_id
         http://localhost:5000/genres/<int:genre_id>/list/new - URL to add new book in genre with id
         http://localhost:5000/genres/<int:genre_id>/list/<int:book_id>/edit - URL to edit a book (with book_id) in the genre with genre_id
         http://localhost:5000/genres/<int:genre_id>/list/<int:book_id>/delete - URL to delete a book (with book_id) in the genre with genre_id
         http://localhost:5000/gconnect - URL for connect to google plus oauth2.0 system to obtain googleplus credentials
         http://localhost:5000/gdisconnect - URL for disconnect from google plus oauth2.0 system



Resources:

1. The details of the books in lotsofbooks.py are obtained from Barnes and noble  (www.bn.com)
2. The background for the home page is downloaded from http://truetowords.blogspot.com/2011_03_01_archive.html
3. I looked up how to add button by using the URL http://css3buttongenerator.com/
