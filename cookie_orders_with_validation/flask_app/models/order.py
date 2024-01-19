
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Order:
    db = "cookies" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Orders Models
    @classmethod
    def create_order(cls,data):
        query = """
        INSERT INTO orders (name, cookie_type, num_of_boxes)
        VALUES (%(name)s,%(cookie_type)s, %(num_of_boxes)s)
        ;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return



    # Read Orders Models
    @classmethod
    def get_one_order(cls, id):
        data = {
            'id' : id
        }
        query = """
        SELECT * FROM orders
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        one_order = cls(results[0])
        return one_order
    
    @classmethod
    def get_all_orders(cls):
        query = """
        SELECT * FROM orders;
        """
        all_orders = []
        results = connectToMySQL(cls.db).query_db(query)
        for order in results:
            all_orders.append(cls(order))
        return all_orders


    # Update Orders Models
    @classmethod
    def update_order(cls, data):
        query = """
        UPDATE orders
        SET name = %(name)s, cookie_type = %(cookie_type)s, num_of_boxes = %(num_of_boxes)s
        WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return

    # Delete Orders Models
    
    # Validation
    @staticmethod
    def validate_order(order):
        is_valid = True
        # test whether a field matches the pattern
        if len(order['name']) < 3:
            flash("Name must be three (3) or more characters long.")
            is_valid = False
        if len(order['cookie_type']) < 3:
            flash("Cookie type must be three (3) or more characters long.")
            is_valid = False
        if int(order['num_of_boxes']) < 0:
            flash("You can't order less than one (1) box.")
            is_valid = False
        return is_valid
        