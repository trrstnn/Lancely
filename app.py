from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, request, abort 
from flask import make_response as response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import fn

import forms 
import models

DEBUG = True
PORT = 9000



app = Flask(__name__)
app.secret_key = 'elsdhfsdlfdsjfkljdslfhjlds'

login_manager = LoginManager() # init instance ofhte LoginManager class
login_manager.init_app(app) ## sets up our login for the app
login_manager.login_view = 'login' # setting default login view as the login function

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# Handle requests when the come in (before) and when they complete (after)
@app.before_request
def before_request():
    # """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    # """Close the database connection after each request."""
    g.db.close()
    return response

## =======================================================
## ROOT ROUTE
## =======================================================

@app.route("/")
def index(name=None):
    if 'auth_token' in session:
    
        return redirect(url_for('layout.html'))
    else: 
        return render_template('splash.html',title="Dashboard", name=name)






## =======================================================
## DELETE WORKOUT ROUTE
## =======================================================

# @app.route("/profile/<workoutid>")
# @login_required
# def delete_workout(workoutid):
#     # form = forms.WorkoutForm()
#     workout = models.Workout.get(workoutid)
#     workout.delete_instance()
#     # workouts = models.Workout.select().where(models.Workout.user == current_user.id)
#     return redirect(url_for('profile'))
#     # return render_template("profile.html", user=current_user, form=form, workouts=workouts)

## =======================================================
## EDIT WORKOUT ROUTE
## =======================================================





@app.route("/profile/")
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    # form = forms.WorkoutForm()
    # workouts = models.Workout.select().where(models.Workout.user == current_user.id)
    
    # if form.validate_on_submit():
    #     models.Workout.create(
    #     name=form.name.data.strip(),
    #     description=form.description.data.strip(), 
    #     user = current_user.id)
    #     return render_template("profile.html", user=current_user, form=form, workouts=workouts)
    return render_template("profile.html", user=current_user)



## =======================================================
## EDIT PROFILE ROUTE
## =======================================================

@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form= forms.UpdateUserForm()
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        user.summary = form.summary.data
        user.category = form.category.data
        user.experience = form.experience.data
        user.skills = form.skills.data
        user.save()
        flash('Your Profile has been updated.') # redirects the user back to the profile page after the form is submitted
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form = form)


## =======================================================
## REGISTER ROUTE
## =======================================================


@app.route('/register', methods = ('GET', 'POST'))
def register():
    form = forms.RegisterForm() # importing the RegisterFrom from forms.py
    if form.validate_on_submit(): #if the data in the form is valid,  then we are gonna create a user
        flash("Successful Signup!", 'Sucess')
        print(form.freelancer.data)
        models.User.create_user(  # calling the create_user function from the user model and passing in the form data
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            name = form.name.data,
            freelancer = form.freelancer.data
            )
        return redirect('/login') # once the submissin is succesful, user is redirected to the index function which routes back to the home page
    return render_template('register.html', form=form)


## =======================================================
## LOGIN ROUTE
## =======================================================

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data) # comparing the user email in the database to the one put in the form
        except models.DoesNotExist:
            flash("your email or password doesn't exist in our database")
        else:   # using the check_password_hash method bc we hashed the user's password when they registered. comparing the user's password in the database to the password put into the form
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user) # this method comes from the flask_login package
                flash("You've been logged in", "success")
                return redirect('/profile')
            else:
                flash("your email or password doesn't match", "error")
    
    return render_template('login.html', form=form)

## =======================================================
## LOGOUT ROUTE
## =======================================================

@app.route('/logout')
@login_required # defines whatever routes and functions are avail when the user is login in aka "Protects the routes"
def logout():
    logout_user() # method that is defined by flask_login
    flash("You've been logged out", "success") , # second argument gives the flash message a class of sucess 
    return redirect(url_for('index'))







@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

    


    

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)

    
