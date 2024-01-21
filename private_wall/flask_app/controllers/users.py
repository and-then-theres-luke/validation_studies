from flask_app import app
from flask_bcrypt import Bcrypt
from flask import request, redirect, render_template, session, flash
from flask_app.models import user, post
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if not session:
        return render_template("index.html")
    return redirect("/home")

##### REGISTRATION ROUTE #####

@app.route("/register", methods=["POST"])
def register_new_user_frontend():
    if not user.User.validate_new_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = user.User.create(data) # This passes back the id number of the last row inserted
    session['user_id'] = user_id
    return redirect("/home")

##### LOGIN ROUTE #####

@app.route("/login", methods=["POST"])
def check_credentials():
    if not user.User.validate_login_inputs(request.form):
        return redirect('/')
    one_user = user.User.get_user_by_email(request.form['email'])
    if not one_user:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash("Invalid email/password", "login")
        return redirect("/")
    session['user_id'] = one_user.id
    return redirect('/home')

##### THE WALL ROUTE #####

@app.route("/home")
def home_frontend():
    if not session:
        return redirect('/')
    one_user = user.User.get_one_user_by_id(session['user_id'])
    all_posts = post.Post.get_all_posts()
    return render_template('dojo_wall.html', one_user = one_user, all_posts = all_posts)

##### POST ROUTES #####

@app.route("/make_post", methods=["POST"])
def make_post_frontend():
    data = {
        'content' : request.form['content'],
        'user_id' : int(request.form['user_id']),
    }
    if not post.Post.validate_new_post(data):
        return redirect("/home")
    post.Post.create(data)
    return redirect("/home")


##### DELETE POST ROUTE #####

@app.route('/delete', methods=["POST"])
def delete_post():
    # I have to do this as a form, if I put the variable in the route it would be chaos
    post.Post.delete(request.form['post_id'])
    return redirect('/home')




##### LOGOUT ROUTE #####

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
