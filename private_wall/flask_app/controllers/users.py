from flask_app import app
from flask_bcrypt import Bcrypt
from flask import request, redirect, render_template, session, flash
from flask_app.models import user, message
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "user_id" not in session:
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
    print(data)
    user_id = user.User.create(data) # This passes back the id number of the last row inserted
    session['user_id'] = user_id
    return redirect("/home")

##### LOGIN ROUTE #####

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

##### THE WALL ROUTE #####

@app.route("/home")
def home_frontend():
    print(session)
    if "user_id" not in session:
        return redirect('/')
    all_users = user.User.get_all_users_minus_current_user(session['user_id'])  # This loads in the current user
    one_user = user.User.get_one_user_by_id(session['user_id'])                 # This loads in everyone else
    one_user.inbox = message.Message.get_all_messages_by_recipient(one_user.id) # this one gets everything in the inbox
    return render_template('dojo_wall.html', one_user = one_user, all_users = all_users)



##### MESSAGE ROUTES #####

@app.route("/send_message", methods=["POST"])
def send_message_frontend():
    data = {
        'sender_id' : session['user_id'],
        'receiver_id' : request.form['receiver_id'],
        'content' : request.form['content']
    }
    message.Message.send_message(data)
    flash("Message sent!", "send_message")
    return redirect('/home')
    
    


##### LOGOUT ROUTE #####

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

