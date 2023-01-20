"""CRUD operations."""

from model import db, Users, Movies, Ratings, connect_to_db


def create_user(email, username, password):
    """Create and return a new user."""
    
    user = Users(email, username, password)
    
    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movies(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )
    
    return movie

def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Ratings(user=user, movie=movie, score=score)

    return rating

def get_all_movies():
    """Gets all Movies from the db"""
    
    return Movies.query.all()

def get_movie_by_id(movie_id):
    return Movies.query.filter_by(movie_id = movie_id).first()

def get_all_users():
    """Gets all Users from the db"""
    
    return Users.query.all()

def get_user_by_id(user_id):
    """gets a user from db based on given id"""
    
    return Users.query.filter_by(user_id=user_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)