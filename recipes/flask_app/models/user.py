
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash, session
import re

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "recipes_database" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        # What changes need to be made above for this project?
        #What needs to be added here for class association?


    ##### CREATE METHOD #####
    
    @classmethod
    def create_user(cls, data):
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
    def get_user_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT *
            FROM users
            LEFT JOIN recipes
            ON users.id = recipes.creator_id
            WHERE users.id = %(id)s
            ;
        """
        one_user = connectToMySQL(cls.db).query_db(query, data) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        user_data = {
            'id' : session['user_id'],
            'first_name' : one_user[0]['first_name'],
            'last_name' : one_user[0]['last_name'],
            'password' : one_user[0]['password'],
            'email' : one_user[0]['email'],
            'created_at' : one_user[0]['created_at'],
            'updated_at' : one_user[0]['updated_at']
        }
        print(user_data)
        list_of_recipes = []
        for row in one_user:
            recipe_data = {
                'id' : row['recipes.id'],
                'creator_id' : row['creator_id'],
                'name' : row['name'],
                'description' : row['description'],
                'instructions' : row['instructions'],
                'made_on' : row['made_on'],
                'under_thirty_minutes' : row['under_thirty_minutes'],
                'created_at' : row['recipes.created_at'],
                'updated_at' : row['recipes.updated_at']
            }
            list_of_recipes.append(recipe.Recipe(recipe_data))
        one_user = cls(user_data)
        one_user.recipes = list_of_recipes
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
            flash("No User Found")
            return False
        return cls(one_user[0])


    ##### UPDATE METHOD #####
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE users
            SET first_name = %(first_name)s, 
            last_name = %(last_name)s, 
            email = %(email)s,
            password = %(password)s,
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
        if not data['email']:
            is_valid = False
            flash("Please input a valid email.", 'login')
        if not data['password']:
            is_valid = False
            flash("Please input a valid password.", 'login')
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address! Use less weird characters. Weirdo. So weird!", 'login')
            is_valid = False
        return is_valid