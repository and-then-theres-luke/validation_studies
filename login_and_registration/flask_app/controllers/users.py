from flask_app import app
from flask_bcrypt import Bcrypt
from flask import request, redirect, render_template, session
from flask_app.models import user
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    all_users = user.User.get_all()
    return render_template("index.html", all_users = all_users)



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
    print("This is session,", session)
    return redirect("/home")



@app.route("/login", methods=["POST"])
def check_credentials():
    one_user = user.User.get_user_by_email(request.form['email'])
    if not one_user:
        flash("Invalid email/password")
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash("Invalid email/password")
        return redirect("/")
    session['user_id'] = one_user.id
    return redirect('/home')



@app.route("/home")
def home_frontend():
    if not session:
        return redirect('/')
    one_user = user.User.get_one_user_by_id(session['user_id'])
    return render_template('homepage.html', one_user = one_user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
