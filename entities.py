

#this is where we store our classes to keep things organized
	
class Movie:
    def __init__(self, movieId, original_title, release_date, overview , vote_average, poster_path):
        self.movieId = movieId
        self.original_title = original_title
        self.release_date = release_date
        self.overview = overview
        self.vote_average = vote_average
        self.poster_path = poster_path
        

#careful, we need to convert album.title to album and artisti.name to artist
class Song:
    def __init__(self, songId, title, artistName, album, cover, preview):
        self.songId = songId
        self.title = title
        self.artistName =  artistName
        self.album = album
        self.cover = cover
        self.preview = preview

class Book:
    def __init__(self, bookId, title, author, thumbnail, description, averageRating):
        self.bookId = bookId
        self.title = title #book.volumeInfo.title
        self.thumbnail=thumbnail #book.volumeInfo.imageLinks.thumbnail
        self.author=author # book.volumeInfo.authors[0]
        self.description=description #book.volumeInfo.description
        self.averageRating=averageRating #book.volumeInfo.averageRating


#utils to convert from json to object
def json2Movie(r):
    fixMissingMovie(r)
    #movieId, original_title, release_date, overview , vote_average, poster_path
    return Movie(r["id"], r["original_title"], r["release_date"], r["overview"], r["vote_average"], r["poster_path"])

def json2Song(r):
    #songId, title, artistName, album, cover, preview
    return Song(r["id"], r["title"],  r["artist"]["name"], r["album"]["title"], r["album"]["cover"], r["preview"])

def json2Book(r):
    r=fixMissingBook(r)
    #bookId, title, author, thumbnail, description, averageRating):
    book =  Book(r["id"], r["volumeInfo"]["title"], r["volumeInfo"]["authors"][0], r["volumeInfo"]["imageLinks"]["thumbnail"], r["volumeInfo"]["description"], r["volumeInfo"]["averageRating"])
    #book = Book(1,2,3,4,5,6)
    return book

def fixMissingMovie(movie):
    #movieId, original_title, release_date, overview , vote_average, poster_path
    if "release_date" not in movie:
        movie["release_date"] = "/"


#fixes missing values from request
def fixMissingBook(book):
    if "imageLinks" not in book["volumeInfo"]:
        book["volumeInfo"]["imageLinks"] = {"thumbnail" : "https://image.shutterstock.com/image-photo/brown-leather-book-cover-600w-169578584.jpg"}
    if "description" in book["volumeInfo"]:
        if len(book["volumeInfo"]["description"]) > 500:
            book["volumeInfo"]["description"] = book["volumeInfo"]["description"][:500] + "..."
    else:
        book["volumeInfo"]["description"] = "*missing description*"
    if "authors" not in book["volumeInfo"]:
        book["volumeInfo"]["authors"] = ["missing_author"]

    if "averageRating" not in book["volumeInfo"]:
        book["volumeInfo"]["averageRating"] = "/"
    
    return book