# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
# model the class after the friend table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Friend:
    db = 'users'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        friends = []
        for person in results:
            friends.append(cls(person))
        return friends

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s
            ;
        """
        that_one_friend = connectToMySQL(cls.db).query_db(query, data) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        return cls(that_one_friend[0])
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        print("The data looks like this (friends.py line 43)", data)
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
    
    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM users
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    @staticmethod
    def validate_friend(new_friend):
        list_of_friends = Friend.get_all()
        is_valid = True
        if len(new_friend['first_name']) < 3:
            flash("First name must be three (3) characters or more.")
            is_valid = False
        if len(new_friend['last_name']) < 3:
            flash("Last name must be three (3) characters or more.")
            is_valid = False
        if len(new_friend['email']) < 3:
            flash("Occupation must be three (3) characters or more.")
            is_valid = False
        for friend in list_of_friends:
            if new_friend['email'] == friend.email:
                flash("Email is already registered to another user.")
                is_valid = False
            else:
                pass
        if not EMAIL_REGEX.match(new_friend['email']): 
            flash("Invalid email address! Use less weird characters. Weirdo. So weird!")
            is_valid = False
        return is_valid
        
        