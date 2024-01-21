from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app import flash
from flask import session


class Post:
    db = 'dojo_wall'
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    
    ##### CREATE METHOD #####
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (content, created_at, updated_at, user_id) VALUES (%(content)s, NOW(), NOW(), %(user_id)s);"
        this_post = connectToMySQL(cls.db).query_db(query, data)
    
    
    
    
    
    ##### READ METHOD #####
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(cls.db).query_db(query) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        all_posts = []
        for row in results:
            all_posts.append(cls(row))
        return all_posts
    
    @classmethod
    def get_all_posts(cls):
        query = """
        SELECT * FROM posts
        JOIN users
        ON posts.user_id = users.id
        ;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_user_posts = []
        for row in results:
            one_post = cls(row)
            one_post_author_info = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            post_creator = user.User(one_post_author_info)
            one_post.creator = post_creator
            all_user_posts.append(one_post)
        return all_user_posts
        
    @classmethod
    def get_all_posts_by_user_id(cls, id):
        data = {
            'id' : id
        }
        query = """
        SELECT * FROM posts
        JOIN users
        ON posts.user_id = users.id
        WHERE users.id = %(id)s
        ;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_user_posts = []
        for row in results:
            one_post = cls(row)
            one_post_info = {
                "id" : row['posts.id'],
                "content" : row['content'],
                "created_at" : row['posts.created_at'],
                "updated_at" : row['posts.updated_at']
            }
            post_creator_info = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            post_creator = user.User(post_creator_info)
            one_post.creator = post_creator
            all_user_posts.append(one_post)
        return results

    @classmethod
    def get_one_post_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT *
            FROM posts
            WHERE id = %(id)s
            ;
        """
        one_post = connectToMySQL(cls.db).query_db(query, data) # The query always returns a list of dictionaries, think [{...},{...}] and these entries are locations in memory.
        return cls(one_post[0])
    
    
    
    
    
    ##### UPDATE METHOD #####
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE posts
            SET content = %(content)s
            WHERE id = %(id)s
            ;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results





    ##### DELETE METHOD #####
    
    @classmethod
    def delete(cls, id):
        data = {
            'id' : id
        }
        query = """
            DELETE FROM posts
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return





    ##### VALIDATION METHODS ######
    
    @staticmethod
    def validate_new_post(new_post):
        is_valid = True
        if len(new_post['content']) < 1:
            flash("The post cannot be blank.", "post")
            is_valid = False
        return is_valid

