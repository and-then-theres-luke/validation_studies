from flask_app import app
from flask import request, redirect, render_template
from flask_app.models import friend

@app.route("/")
def index():
    return redirect("/read")

@app.route("/read")
def read():
    returned_dictionary = friend.Friend.get_all()
    all_friends = []
    for item in returned_dictionary:
        all_friends.append(item)
    return render_template("read.html", all_friends = all_friends)

@app.route("/read/<int:id>")
def read_one(id):
    data = {"id" : id}
    one_friend = friend.Friend.get_one(data)
    return render_template("read_one.html", one_friend = one_friend)

@app.route("/edit/<int:id>")
def edit(id):
    data = {
        'id' : id
    }
    one_friend = friend.Friend.get_one(data)
    return render_template("edit.html", one_friend = one_friend)

@app.route("/update", methods=["POST"])
def update():
    friend.Friend.update(request.form)
    return redirect('/read')
    
@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/create/process", methods=["POST"])
def create_process():
    if not friend.Friend.validate_friend(request.form):
        return redirect("/create")
    new_friend = friend.Friend.create(request.form)
    redirect_string = f"""/read/{new_friend}"""
    return redirect(redirect_string)
        
    
    

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        'id' : id
    }
    friend.Friend.delete(data)
    return redirect('/')