from matplotlib.style import use
from database import get_db, close_db   

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




class DatabaseManager:
        def __init__(self, dbFile):
            self.dbfile = dbFile

        def add_movie(self, movie, userId):
            #connect
            db = get_db()

            #check if exists
            query = """
                    SELECT *
                    FROM movies
                    WHERE (movieId = ? AND userId = ?)    
                    """
            exists = db.execute(query, (movie.movieId, userId)).fetchone()

            if exists is not None:
                er = "user exists"
            
            else:
                query ="""
                        INSERT INTO movies (userId, movieId, original_title, release_date, overview , vote_average, poster_path)
                        VALUES (?,?,?,?,?,?,?);
                        """
                db.execute(query, (userId, movie.movieId, movie.original_title, movie.release_date, movie.overview , movie.vote_average, movie.poster_path))
                db.commit()
                message= "Movie inserted"

            return 0





""" TODO remove this
{% for book in bookList %}
    <div class="col">
        <div class="card h-100">
            <img src='{{ book.volumeInfo.imageLinks.thumbnail }}' class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">{{  book.volumeInfo.title }} </h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ book.volumeInfo.authors[0] }} - {{ book.volumeInfo.c }}</h6>
                <a href="#" class="btn btn-warning"><img src="{{ url_for('static', filename='star-fill.svg') }}" alt="Add movie"></a>
                <p class="card-text">{{ book.volumeInfo.description }} </p>
            </div>
            <div class="card-footer"> <small class="text-muted"><b>Rating:</b> {{ book.volumeInfo.averageRating }}</small> </div>
            
        </div>
    </div>
    {% endfor %}


        {% for track in trackList %}
    <div class="col">
        <div class="card h-100">
            <img src="{{ track.album.cover_medium }}" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">{{ track.title }} </h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ track.artist.name }} - {{ track.album.title }}</h6>
                <a href="#" class="btn btn-warning"><img src="{{ url_for('static', filename='star-fill.svg') }}" alt="Add music"></a>
            </div>
            <div class="card-footer"><audio class="w-75 p-3" controls src="{{ track.preview }}" > </audio></div>
        </div>
    </div>
    {% endfor %}


"""