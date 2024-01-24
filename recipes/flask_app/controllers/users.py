from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

##### ROOT CONTROLLER ##### WORKING

@app.route('/')
def index():
    if "user_id" not in session:
        return render_template('login.html')
    return redirect('/home')

##### LOGIN CONTROLLER ##### WORKING

@app.route("/login", methods=["POST"])
def check_credentials():
    if not user.User.validate_login_inputs(request.form):
        return redirect('/')
    one_user = user.User.get_user_by_email(request.form['email']) # Returns user object
    if not one_user:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash("Invalid email/password", "login")
        return redirect("/")
    session['user_id'] = one_user.id
    return redirect('/home')

##### REGISTRATION CONTROLLER ##### WORKING

@app.route('/register', methods=["POST"])
def register_frontend():
    if not user.User.validate_new_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    hashed_user = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = user.User.create_user(hashed_user)
    session['user_id'] = user_id
    return redirect('/home')
    

##### HOMEPAGE CONTROLLER #####

@app.route('/home')
def home_frontend():
    if 'user_id' not in session:
        flash("Please login to access this page.", "access")
        return redirect('/')
    one_user = user.User.get_user_by_id(session['user_id']) # This returns a user object with recipes attached
    all_recipes = recipe.Recipe.get_all_recipes()
    return render_template('recipes.html', one_user = one_user, all_recipes = all_recipes)

##### SHOW ONE RECIPE CONTROLLER #####

@app.route('/recipe/<int:recipe_id>')
def show_one_recipe_frontend(recipe_id):
    if 'user_id' not in session:
        flash("Please login to access this page.", "access")
        return redirect('/')
    one_user = user.User.get_user_by_id(session['user_id'])
    one_recipe = recipe.Recipe.get_one_recipe_by_recipe_id(recipe_id)
    return render_template("one_recipe.html", one_user = one_user, one_recipe = one_recipe)

##### EDIT RECIPES CONTROLLER #####

@app.route('/edit/<int:recipe_id>')
def edit_one_recipe_frontend(recipe_id):
    if 'user_id' not in session:
        flash("Please login to access this page.", "access")
        return redirect('/')
    one_user = user.User.get_user_by_id(session['user_id'])
    one_recipe = recipe.Recipe.get_one_recipe_by_recipe_id(recipe_id)
    return render_template("edit_recipe.html", one_user = one_user, one_recipe = one_recipe)

@app.route('/edit/process', methods=["POST"])
def edit_one_recipe_process_frontend():
    if not recipe.Recipe.validate_recipe(request.form):
        redirect_string = f"""/edit/{request.form['id']}"""
        return redirect(redirect_string)
    recipe.Recipe.update(request.form)
    return redirect('/home')

##### LOGOUT AND CLEAR SESSION #####

@app.route('/logout')
def logout_frontend():
    session.clear()
    return redirect('/')

##### CREATE RECIPE CONTROLLERS #####

@app.route('/create')
def create_frontend():
    if 'user_id' not in session:
        flash("Please login to access this page.", "access")
        return redirect('/')
    return render_template('create.html')

@app.route('/create/process', methods=['POST'])
def create_process_frontend():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/create')
    recipe.Recipe.create_recipe(request.form)
    return redirect('/home')



