
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Recipe:
    db = "recipes_database" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.creator_id = data['creator_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['made_on']
        self.under_thirty_minutes = data['under_thirty_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    ##### CREATE MODELS #####
    
    @classmethod
    def create_recipe(cls,data):
        query = """
        INSERT INTO recipes 
        (creator_id, name, description, instructions, made_on, under_thirty_minutes, created_at, updated_at)
        VALUES 
        (%(creator_id)s, %(name)s, %(description)s, %(instructions)s, %(made_on)s, %(under_thirty_minutes)s, NOW(), NOW())
        ;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return


    ##### READ MODELS #####
    
    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.creator_id
        ;
        """
        results = connectToMySQL(cls.db).query_db(query)
        list_of_recipes = []
        for row in results:
            recipe_data = {
                'id' : row['id'],
                'creator_id' : row['creator_id'],
                'name' : row['name'],
                'description' : row['description'],
                'instructions' : row['instructions'],
                'made_on' : row['made_on'],
                'under_thirty_minutes' : row['under_thirty_minutes'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            one_recipe = cls(recipe_data)
            creator_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            one_recipe.creator = user.User(creator_data)
            list_of_recipes.append(one_recipe)
        return list_of_recipes
    
    @classmethod
    def get_one_recipe_by_recipe_id(cls,id):
        data = {
            'id' : id
        }
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.creator_id
        WHERE recipes.id = %(id)s
        ;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        recipe_data = {
                'id' : results[0]['id'],
                'creator_id' : results[0]['creator_id'],
                'name' : results[0]['name'],
                'description' : results[0]['description'],
                'instructions' : results[0]['instructions'],
                'made_on' : results[0]['made_on'],
                'under_thirty_minutes' : results[0]['under_thirty_minutes'],
                'created_at' : results[0]['created_at'],
                'updated_at' : results[0]['updated_at']
        }
        one_recipe = cls(recipe_data)
        creator_data = {
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'password' : results[0]['password'],
                'email' : results[0]['email'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
        one_recipe.creator = user.User(creator_data)
        return one_recipe


    ##### UPDATE MODELS #####
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes
            SET name = %(name)s, 
            description = %(description)s, 
            instructions = %(instructions)s, 
            made_on = %(made_on)s, 
            under_thirty_minutes = %(under_thirty_minutes)s, 
            created_at = %(created_at)s, 
            updated_at = %(updated_at)s, 
            creator_id = %(creator_id)s
            WHERE id = %(id)s
            ;
        """
        
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    ##### DELETE MODELS #####
    @classmethod
    def delete_recipe_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            DELETE FROM recipes
            WHERE id = %(id)s
            ;
            """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    ##### VALIDATION METHODS #####
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        print("We're validating now!")
        print("request.form:::", recipe)
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Recipe name needs to be three (3) characters or longer.", "recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Recipe description needs to be three (3) characters or longer.", "recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Recipe instructions need to be three (3) characters or longer.", "recipe")
        if 'under_thirty_minutes' not in recipe:
            is_valid = False
            flash("Does this recipe take 30 minutes or less? Please select...", "recipe")
        return is_valid
    
