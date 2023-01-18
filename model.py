"""Models for movie ratings app."""
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    
    # ratings = a list of Rating objects

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        
class Movies(db.Model):
    '''A movie'''
    
    __tablename__ = 'movies'
    
    movie_id = db.Column(db.Integer, autoincrement= True, primary_key = True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)
    
    # ratings = a list of Rating objects
    
    def __repr__(self):
        return f"<Movie movie_id={self.movie_id} title={self.title}>"
    
class Ratings(db.Model):
    """Movie ratings"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    movie = db.relationship("Movies", backref="ratings")
    user = db.relationship("Users", backref="ratings")
    
    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print('Connected to db...')