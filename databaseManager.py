from database import get_db, close_db   
from entities import Movie, Song, Book

#CRUD operations

def get_movies(userId):
    db = get_db()

    query = """
            SELECT *
            FROM movies
            WHERE userId = ?    
            """
    
    results = db.execute(query, (userId,)).fetchall()

    movies = [Movie(r[1], r[2], r[3], r[4], r[5], r[6]) for r in results]

    return movies

def add_movie(movie, userId):
    print("hello")
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
        er = "entry exists"

    else:
        query ="""
                INSERT INTO movies (userId, movieId, original_title, release_date, overview , vote_average, poster_path)
                VALUES (?,?,?,?,?,?,?);
                """
        db.execute(query, (userId, movie.movieId, movie.original_title, movie.release_date, movie.overview , movie.vote_average, movie.poster_path))
        db.commit()
        message= "Movie inserted"
    return 0

def remove_movie(movieId, userId):
    db = get_db()
    query = """
            DELETE
            FROM movies
            WHERE (movieId = ? AND userId = ?)   
            """
    db.execute(query, (movieId, userId))
    db.commit()

#SONGS #########

def get_songs(userId):
    db = get_db()

    query = """
            SELECT *
            FROM songs
            WHERE userId = ?    
            """
    
    results = db.execute(query, (userId,)).fetchall()

    print("hey")
    songs = [Song(r[1], r[2], r[3], r[4], r[5], r[6]) for r in results]

    return songs

def add_song(song, userId):
    print("hello")
    #connect
    db = get_db()

    #check if exists
    query = """
            SELECT *
            FROM songs
            WHERE (songId = ? AND userId = ?)    
            """
    exists = db.execute(query, (song.songId, userId)).fetchone()

    if exists is not None:
        er = "entry exists"

    else:
        query ="""
                INSERT INTO songs (userId, songId, title, artistName, album, cover, preview)
                VALUES (?,?,?,?,?,?,?);
                """
        db.execute(query, (userId, song.songId, song.title, song.artistName, song.album, song.cover, song.preview))
        db.commit()
        message= "Movie inserted"
    return 0

def remove_song(songId, userId):
    db = get_db()
    query = """
            DELETE
            FROM songs
            WHERE (songId = ? AND userId = ?)   
            """
    db.execute(query, (songId, userId))
    db.commit()

#BOOKS ########3

def get_books(userId):
    db = get_db()

    query = """
            SELECT *
            FROM books
            WHERE userId = ?    
            """
    
    results = db.execute(query, (userId,)).fetchall()

    books = [Book(r[1], r[2], r[3], r[4], r[5], r[6]) for r in results]

    return books

def add_book(book, userId):
    print("hello")
    #connect
    db = get_db()

    #check if exists
    query = """
            SELECT *
            FROM books
            WHERE (bookId = ? AND userId = ?)    
            """
    exists = db.execute(query, (book.bookId, userId)).fetchone()

    if exists is not None:
        er = "entry exists"

    else:
        query ="""
                INSERT INTO books (userId, bookId, title, author, thumbnail, description, averageRating) 
                VALUES (?,?,?,?,?,?,?);
                """
        db.execute(query, (userId, book.bookId, book.title, book.author, book.thumbnail, book.description, book.averageRating))
        db.commit()
        message= "book inserted"
    return 0

def remove_book(bookId, userId):
    db = get_db()
    query = """
            DELETE
            FROM books
            WHERE (bookId = ? AND userId = ?)   
            """
    db.execute(query, (bookId, userId))
    db.commit()