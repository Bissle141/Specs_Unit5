"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
from jinja2 import StrictUndefined
import os
import crud

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    
    return render_template('hompage.html')

@app.route('/movies')
def movies():
    """View all movies"""
    
    movies = crud.get_all_movies()
    
    return render_template('movies.html', movies = movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie"""
    
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template('movie_details.html', movie= movie)
    
@app.route('/users')
def users():
    """View all users"""

    return render_template('users.html', users=crud.get_all_users())

@app.route('/users/<user_id>')
def user_profile(user_id):
    """displays a users profile"""
    
    return render_template('profile.html', user= crud.get_user_by_id(user_id))

@app.route('/login')
def login_logout():
    if 'user' in session:
        del session['user']
        
        return redirect('/')
    
    return render_template('login.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
