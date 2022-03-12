import requests
from flask import Flask, render_template, request
from forms import MovieSearch, MusicSearch, BookSearch

from database import get_db, close_db
from entities import Movie, Song, Book, DatabaseManager


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

        print(trackList[0])
            
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

        #fix missing images, crop description, missing author
        for book in resList:
            if "imageLinks" not in book["volumeInfo"]:
                book["volumeInfo"]["imageLinks"] = {"thumbnail" : "https://image.shutterstock.com/image-photo/brown-leather-book-cover-600w-169578584.jpg"}
            if "description" in book["volumeInfo"]:
                if len(book["volumeInfo"]["description"]) > 500:
                    book["volumeInfo"]["description"] = book["volumeInfo"]["description"][:500] + "..."
            if "authors" not in book["volumeInfo"]:
                book["volumeInfo"]["authors"] = ["missing_author"]

    return render_template("bookSelection.html", form=form, bookList=resList)


#save movies to database
@app.route("/addMovie/<movieId>")
def addMovie(movieId):
    url = f"https://api.themoviedb.org/3/movie/{movieId}"
    paramDict = {"api_key": TMDB_APIEKY, "language":"en-US"}
    movieReq = requests.get(url, params=paramDict).json()

    #make object
    movie = Movie()

    DatabaseManager.add_movie(movie, userId=1)

    return 0


@app.route("/shift", methods=["GET", "POST"])
def cipher():
    form = CaesarShift()
    if form.validate_on_submit():
        plainText = form.plainText.data
        shift = form.shift.data
        form.cipher.data = makeCipher(plainText, shift)
    return render_template("shift_form.html", form=form)
    
@app.route("/conversion", methods=["GET", "POST"])
def conversion():
    form = TemperatureConversion()
    if form.validate_on_submit():
        unitFrom = form.unitFrom.data
        temperature = float(form.temperature.data)
        unitTo = form.unitTo.data

        #print(unitFrom, float(temperature)*1.0, unitTo)
        form.converted.data = convertTemperature(unitFrom, unitTo, temperature)
    return render_template("conversion_form.html", form=form)
    

def convertTemperature(unitFrom, unitTo, temperature):
    converted = float(temperature)
    if unitFrom == "Celsius":
        if unitTo == "Kelvin":
            converted = temperature + 273
        elif unitTo == "Fahrenheit":
            converted = 9/5 * temperature + 32
    elif unitFrom == "Kelvin":
        if unitTo == "Celsius":
            converted = temperature - 273
        elif unitTo == "Fahrenheit":
            converted = 9/5 * (temperature - 273) + 32
    elif unitFrom == "Fahrenheit":
        if unitTo == "Celsius":
            converted =5/9 * (temperature - 32)
        elif unitTo == "Kelvin":
            converted = 5/9 * (temperature - 32) + 273

    return converted

def makeCipher(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext
