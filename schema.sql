DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    userId INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password)
VALUES ('luka', 'pass');

--TODO foreign userid, which user added it
    -- userId INTEGER NOT NULL,
    -- FOREIGN KEY (userId)
    --    REFERENCES users (userId) 


--maybe its more correct PRIMARY KEY (movieId, userId)
-- TODO check SQL best way

--saved movies
DROP TABLE IF EXISTS movies;

CREATE TABLE movies
(
    userId INTEGER NOT NULL,
    movieId TEXT NOT NULL,
    
    original_title TEXT NOT NULL,
    release_date TEXT NOT NULL,
    overview TEXT NOT NULL,
    vote_average TEXT NOT NULL, 
    poster_path TEXT NOT NULL,
    
    PRIMARY KEY (movieId, userId)
);

-- INSERT INTO movies (userId, movieId, original_title, release_date, overview , vote_average, poster_path)
-- VALUES (1,121,'The Lord of the Rings: The Two Towers','vote_average','testt','8.4','/nSNle6UJNNuEbglNvXt67m1a1Yn.jpg');


--saved songs
DROP TABLE IF EXISTS songs;

CREATE TABLE songs
(
    userId INTEGER NOT NULL,
    songId TEXT NOT NULL,
    
    title TEXT NOT NULL,
    artistName TEXT NOT NULL,
    album TEXT NOT NULL,
    cover TEXT NOT NULL,
    preview TEXT NOT NULL,

    PRIMARY KEY (songId, userId)
);
--saved books
DROP TABLE IF EXISTS books;

CREATE TABLE books
(   
    userId INTEGER NOT NULL,
    bookId TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    thumbnail TEXT NOT NULL,
    description TEXT NOT NULL,
    averageRating TEXT NOT NULL,

    PRIMARY KEY (bookId, userId)
);

