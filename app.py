from distutils.log import Log
from functools import wraps

import requests
from flask import Flask, redirect, render_template, request, session, url_for, g
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import MovieSearch, MusicSearch, BookSearch, LoginForm, RegisterForm

from database import get_db, close_db
from entities import Movie, Song, Book, fixMissingBook, json2Book, json2Movie, json2Song
import databaseManager as dbm #here we store the functions for inserting and deleting

"""
Downtime organizer
Search for any movie/song/book, and add it to your collection of stuff you want to do during your downtime, all in one place.
Instructions: register a new user and login. You will see an empty collection of movies, songs and books. To add stuff click on Movies/Music/Books,
search for what you want and click the yellow star button. It will now appear in your collection under the appropriate category. 
When you finished watching the movie, simply remove it from the collection, by clicking the yellow button, with the filled star.
Alternatively there is some stuff I like already saved under username:admin password:admin
"""

app=Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "secret-keyy"
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

#tmdb api key
TMDB_APIEKY = "bf3d84686c3cb07442af95ea036a10e6"

@app.before_request
def load_logged_in_user():
    g.user = session.get("userId", None)
    g.username = session.get("username", None)

def loginRequired(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        query = """ SELECT * FROM users WHERE username = ? """
        exists = db.execute(query, (username,)).fetchone()
        if exists is not None:
            form.username.errors.append("username already taken")
        else:
            db.execute(""" INSERT INTO users (username, password) VALUES (?,?); """, (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session: return redirect(url_for("collections")) #skip the login page if the user is logged in
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        query = """ SELECT * FROM users WHERE username = ? """
        exists = db.execute(query, (username,)).fetchone()
        if exists is None:
            form.username.errors.append("username doesnt exist")
        elif not check_password_hash(exists["password"], password):
            form.password.errors.append("Wrong password!")
        else:
            session.clear()
            session["username"] = username
            session["userId"] = exists[0]
            print(session["userId"])
            next_page = request.args.get("next")
            #we can redirect to next_page, but collections is cleaner
            return redirect(url_for("collections"))

    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/movies", methods=["GET", "POST"])
@loginRequired
def searchMovies():
    #list of found search results
    listMovies = []

    form = MovieSearch()
    
    #make a request to find movies
    if form.validate_on_submit():
        #title of movie we want to find
        searchString = form.movieTitle.data
        #url parameters
        paramDict = {"api_key": TMDB_APIEKY , "language":"en-US", "query":searchString, "page":1, "include_adult":"false"}
        req = requests.get("https://api.themoviedb.org/3/search/movie", params=paramDict)
        
        #convert response into list of movies - dictionaries
        listMovies = req.json().get("results")

        #convert to objects of class Movie
        listMovies = [json2Movie(r) for r in listMovies]
            
    return render_template("movieSelection.html", form=form, listMovies=listMovies)

#search for songs
@app.route("/music", methods=["GET", "POST"])
@loginRequired
def searchMusic():
    #list of found search results
    trackList = []
    form = MusicSearch()

    if form.validate_on_submit():
        url="https://api.deezer.com/search"
        searchString = form.searchString.data
        paramDict = {"q":searchString}
        req = requests.get(url, params=paramDict)

        trackList = req.json().get("data")

        trackList = [json2Song(r) for r in trackList]
            
    return render_template("musicSelection.html", form=form, trackList=trackList)

#search for books
@app.route("/books", methods=["GET", "POST"])
@loginRequired
def searchBooks():
    #list of found search results
    resList = []
    form = BookSearch()

    if form.validate_on_submit():
        url='https://www.googleapis.com/books/v1/volumes?'
        searchString = form.searchString.data
        paramDict = {"q":searchString, "maxResults":16}
        req = requests.get(url, params=paramDict)
        resList = req.json()["items"]

        resList = [json2Book(r) for r in resList]

    return render_template("bookSelection.html", form=form, bookList=resList)


#save movies to database
@app.route("/addMovie/<movieId>", methods=["GET", "POST"])
@loginRequired
def addMovie(movieId, userId=1):
    url = f"https://api.themoviedb.org/3/movie/{movieId}"
    paramDict = {"api_key": TMDB_APIEKY, "language":"en-US"}
    movieReq = requests.get(url, params=paramDict).json()

    #make object
    movie = json2Movie(movieReq) #convert json 2 object
    print(movie.original_title)
    dbm.add_movie(movie=movie, userId=session["userId"])
    
    return redirect(url_for("collections"))

#delete movie
@app.route("/removeMovie/<movieId>", methods=["GET", "POST"])
@loginRequired
def removeMovie(movieId, userId=1):
    dbm.remove_movie(movieId=movieId, userId=session["userId"])
    return redirect(url_for("collections"))

#save song
@app.route("/addSong/<songId>", methods=["GET", "POST"])
@loginRequired
def addSong(songId, userId=1):
    url = f"https://api.deezer.com/track/{songId}"
    req = requests.get(url).json()

    #make object
    song = json2Song(req) #convert json 2 object

    dbm.add_song(song=song, userId=session["userId"])
    
    return redirect(url_for("collections"))

#delete song
@app.route("/removeSong/<songId>", methods=["GET", "POST"])
@loginRequired
def removeSong(songId, userId=1):
    dbm.remove_song(songId=songId, userId=session["userId"])
    return redirect(url_for("collections"))

#ssve book
@app.route("/addBook/<bookId>", methods=["GET", "POST"])
@loginRequired
def addBook(bookId, userId=1):
    url=f'https://www.googleapis.com/books/v1/volumes/{bookId}'
    req = requests.get(url)
    r = req.json()

    #make object
    book = json2Book(r) #convert json 2 object
    dbm.add_book(book=book, userId=session["userId"])
    
    return redirect(url_for("collections"))

#delete book
@app.route("/removeBook/<bookId>", methods=["GET", "POST"])
@loginRequired
def removeBook(bookId, userId=1):
    dbm.remove_book(bookId=bookId, userId=session["userId"])
    return redirect(url_for("collections"))

#show the users collection
@app.route("/collections", methods=["GET", "POST"])
@loginRequired
def collections():
    userId = session["userId"]
    listMovies = dbm.get_movies(userId=userId)
    trackList = dbm.get_songs(userId=userId)
    bookList = dbm.get_books(userId=userId)
    return render_template("collections.html", listMovies=listMovies, trackList=trackList, bookList=bookList)
