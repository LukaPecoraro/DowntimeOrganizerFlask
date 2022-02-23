import requests
from flask import Flask, render_template, request

from forms import CaesarShift, TemperatureConversion, MovieSearch, MusicSearch

app=Flask(__name__)
app.config["SECRET_KEY"] = "secret-keyy"

#tmdb api key
TMDB_APIEKY = "bf3d84686c3cb07442af95ea036a10e6"

@app.route("/")
def home():
    return "Hello, please go to url"


@app.route("/movies", methods=["GET", "POST"])
def seaarchMovie():
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
