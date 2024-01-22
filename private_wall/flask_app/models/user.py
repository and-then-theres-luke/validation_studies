# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message
from flask_app import flash
from flask import session, redirect
import re
# model the class after the user table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db = 'dojo_wall'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.inbox = []
    # Now we use class methods to query our database
    

    
    ##### CREATE METHOD #####
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    ##### READ METHODS #####
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        users = []
        for person in results:
            users.append(cls(person))
        return users



    @classmethod
    def get_one_user_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s
            ;
        """
        one_user = connectToMySQL(cls.db).query_db(query, data) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        one_user = cls(one_user[0])
        return one_user
    
    @classmethod
    def get_user_by_email(cls,email):
        data = {
            'email' : email
        }
        query = """
            SELECT * 
            FROM users 
            WHERE email = %(email)s
            ;
        """
        one_user = connectToMySQL(cls.db).query_db(query, data)
        if not one_user:
            flash("")
            return redirect('/')
        return cls(one_user[0])
    
    ##### UPDATE METHOD ######
    
    @classmethod
    def update(cls, data):
        print("The data looks like this (users.py line 43)", data)
        query = """
            UPDATE users
            SET first_name = %(first_name)s, 
            last_name = %(last_name)s, 
            occupation = %(email)s
            WHERE id = %(id)s
            ;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print("The results of the update are", results)
        return results
    
    ###### DELETE METHOD ######
    
    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM users
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    ##### VALIDATION METHODS #####
    
    @staticmethod
    def validate_new_user(new_user):
        list_of_users = User.get_all_users()
        is_valid = True
        if len(new_user['first_name']) < 3:
            flash("First name must be three (3) characters or more.", "register")
            is_valid = False
        if len(new_user['last_name']) < 3:
            flash("Last name must be three (3) characters or more.", "register")
            is_valid = False
        if len(new_user['email']) < 3:
            flash("Occupation must be three (3) characters or more.", "register")
            is_valid = False
        for user in list_of_users:
            if new_user['email'] == user.email:
                flash("Email is already registered to another user.", "register")
                is_valid = False
            else:
                pass
        if not EMAIL_REGEX.match(new_user['email']): 
            flash("Invalid email address! Use less weird characters. Weirdo. So weird!", "register")
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash("The passwords don't match! Try again.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login_inputs(data):
        is_valid = True
        list_of_users = User.get_all_users()
        if not data['email']:
            is_valid = False
            flash("Please input a valid email.", 'login')
        if not data['password']:
            is_valid = False
            flash("Please input a valid password.", 'login')
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address! Use less weird characters. Weirdo. So weird!", 'login')
            is_valid = False
        is_valid = False
        for user in list_of_users:
            if data['email'] == user.email:
                is_valid = True
            else:
                pass
        if not is_valid:
            flash("No user registered with that particular email.", 'login')
        return is_valid