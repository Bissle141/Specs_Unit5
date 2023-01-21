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
    ratings = crud.get_ratings_for_movie(movie_id)
    
    return render_template('movie_details.html', movie= movie, ratings=ratings)
    
@app.route('/users')
def users():
    """View all users"""

    return render_template('users.html', users=crud.get_all_users())

@app.route('/users/<user_id>')
def user_profile(user_id):
    """displays a users profile"""
    
    return render_template('profile.html', user= crud.get_user_by_id(user_id))

@app.route('/login', methods=["POST", "GET"])
def login_logout():
    if 'user_id' in session:
        del session['user_id']
        
        return redirect('/')
    
    if request.form:
        email = request.form['email']
        password = request.form['password']
    
        user = crud.get_user_by_email(email)
        
        if user is not None: 
            if password == user.password:
                session['user_id'] = user.user_id
                flash('Logged in')
                return redirect(url_for('homepage'))
            else:
                flash('Incorect password, please try again')
                return redirect(url_for('login_logout'))
        else:
            flash('User does not exist')
        
    return render_template('login.html')

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    
    email, username, password = request.form['email'], request.form['username'], request.form['password']
    
    if crud.get_user_by_email(email) == None:
        user = crud.create_user(email, username, password)
        
        db.session.add(user)
        db.session.commit()
        
        flash("Sucessfully registered. Please log in.")
        return redirect(url_for('login_logout'))
    else:
        flash("Email is already in use.")
        return redirect(url_for('login_logout'))

@app.route('/rate/<movie_id>', methods=["POST"])
def rate_movie(movie_id):
    if 'user_id' not in session:
        flash('Must be signed in to rate a movie.')
        return redirect(url_for('login_logout'))
    
    score = request.form['rating']
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session['user_id'])
    
    print(movie.movie_id)
    
    rating = crud.create_rating(user, movie, score)
    
    db.session.add(rating)
    db.session.commit()
    
    flash("Movie Rated")
    return redirect(f'/movies/{movie.movie_id}')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
