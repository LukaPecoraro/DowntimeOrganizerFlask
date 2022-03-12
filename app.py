from matplotlib.style import use
import requests
from flask import Flask, redirect, render_template, request, url_for
from forms import MovieSearch, MusicSearch, BookSearch

from database import get_db, close_db
from entities import Movie, Song, Book, fixMissingBook, json2Book, json2Movie, json2Song
import databaseManager as dbm #here we store the functions for inserting and deleting


app=Flask(__name__)
app.config["SECRET_KEY"] = "secret-keyy"

#tmdb api key
TMDB_APIEKY = "bf3d84686c3cb07442af95ea036a10e6"

@app.route("/")
def home():
    return "Hello, please go to url"


@app.route("/movies", methods=["GET", "POST"])
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

        listMovies = [json2Movie(r) for r in listMovies]
            
    return render_template("movieSelection.html", form=form, listMovies=listMovies)

@app.route("/music", methods=["GET", "POST"])
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


@app.route("/books", methods=["GET", "POST"])
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
def addMovie(movieId, userId=1):
    url = f"https://api.themoviedb.org/3/movie/{movieId}"
    paramDict = {"api_key": TMDB_APIEKY, "language":"en-US"}
    movieReq = requests.get(url, params=paramDict).json()

    #make object
    movie = json2Movie(movieReq) #get correct from html
    print(movie.original_title)
    dbm.add_movie(movie=movie, userId=userId)
    
    return redirect(url_for("collections"))

#delete movie
@app.route("/removeMovie/<movieId>", methods=["GET", "POST"])
def removeMovie(movieId, userId=1):
    dbm.remove_movie(movieId=movieId, userId=userId)
    return redirect(url_for("collections"))

#save song
@app.route("/addSong/<songId>", methods=["GET", "POST"])
def addSong(songId, userId=1):
    url = f"https://api.deezer.com/track/{songId}"
    req = requests.get(url).json()

    #make object
    song = json2Song(req) #get correct from json

    dbm.add_song(song=song, userId=userId)
    
    return redirect(url_for("collections"))

#delete song
@app.route("/removeSong/<songId>", methods=["GET", "POST"])
def removeSong(songId, userId=1):
    dbm.remove_song(songId=songId, userId=userId)
    return redirect(url_for("collections"))

#ssve book
@app.route("/addBook/<bookId>", methods=["GET", "POST"])
def addBook(bookId, userId=1):
    url=f'https://www.googleapis.com/books/v1/volumes/{bookId}'
    req = requests.get(url)
    r = req.json()

    #make object
    book = json2Book(r) #get correct from json
    dbm.add_book(book=book, userId=userId)
    
    return redirect(url_for("collections"))

#delete book
@app.route("/removeBook/<bookId>", methods=["GET", "POST"])
def removeBook(bookId, userId=1):
    dbm.remove_book(bookId=bookId, userId=userId)
    return redirect(url_for("collections"))

#show the users collection
@app.route("/collections", methods=["GET", "POST"])
def collections():
    listMovies = dbm.get_movies(userId=1)
    trackList = dbm.get_songs(userId=1)
    bookList = dbm.get_books(userId=1)
    return render_template("collections.html", listMovies=listMovies, trackList=trackList, bookList=bookList)
