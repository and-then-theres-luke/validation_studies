from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import order # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Orders Controller

@app.route('/cookies/new')
def create_order_frontend():
    return render_template("new_order.html")

@app.route('/cookies/new/process', methods=["POST"])
def create_order_process_frontend():
    if not order.Order.validate_order(request.form):
        return redirect("/cookies/new")
    order.Order.create_order(request.form)
    return redirect('/cookies')

# Read Orders Controller

@app.route('/')
def index():
    return redirect("/cookies")

@app.route('/cookies')
def all_orders_frontend():
    all_orders = order.Order.get_all_orders()
    return render_template('all_orders.html', all_orders = all_orders)


# Update Orders Controller

@app.route('/cookies/edit/<int:id>')
def edit_order_frontend(id):
    one_order = order.Order.get_one_order(id)
    return render_template('change_order.html', one_order = one_order)

@app.route('/cookies/edit/process', methods=["POST"])
def edit_order_process_frontend():
    if not order.Order.validate_order(request.form):
        return_string = f"""/cookies/edit/{request.form['id']}"""
        return redirect(return_string)
    order.Order.update_order(request.form)
    return redirect('/cookies')


# Delete Orders Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.