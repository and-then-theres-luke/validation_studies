from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app import flash
from flask import session


class Message:
    db = 'private_wall'
    def __init__( self , data ):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.receiver = None
    
    
    ##### CREATE METHOD #####
    
    @classmethod
    def send_message(cls, data):
        query = """INSERT INTO messages (sender_id, receiver_id, content, created_at, updated_at) 
        VALUES (%(sender_id)s, %(receiver_id)s, %(content)s, NOW(), NOW())
        ;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    
    
    ##### READ METHOD #####
    
    @classmethod
    def get_all_messages_by_sender(cls, sender_id):
        data = {
            'id' : sender_id
        }
        query = """
        SELECT * FROM users
        LEFT JOIN messages
        ON users.id = messages.sender_id
        WHERE users.id = %(id)s;
        """
        all_messages_by_sender = []
        results = connectToMySQL(cls.db).query_db(query, data)
        for one_message in results:
            all_messages_by_sender.append(cls(one_message))
        return all_messages_by_sender
    
    @classmethod
    def get_all_messages_by_recipient(cls,id):
        data = {
            'id' : id
            }
        query = """
        SELECT * FROM users AS sender 
        JOIN messages 
        ON sender.id = messages.sender_id 
        JOIN users AS receiver 
        ON messages.receiver_id = receiver.id
        WHERE receiver.id = %(id)s
        ;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        inbox = []
        for row in results:
            message_data = {
                'id' : row['messages.id'],
                'content' : row['content'],
                'receiver_id' : row['receiver_id'],
                'sender_id' : row['sender_id'],
                'created_at' : row['messages.created_at'],
                'updated_at' : row['messages.updated_at']
            }
            populated_message = cls(message_data)
            sender_data = {
                'id' : row['id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at'],
                'email' : row['email']
            }
            receiver_data = {
                'id' : row['receiver.id'],
                'first_name' : row['receiver.first_name'],
                'last_name' : row['receiver.last_name'],
                'password' : row['receiver.password'],
                'created_at' : row['receiver.created_at'],
                'updated_at' : row['receiver.updated_at'],
                'email' : row['receiver.email']
            }
            populated_message.sender = user.User(sender_data)
            populated_message.receiver = user.User(receiver_data)
            print("POPULATE MESSAGE:", populated_message)
            inbox.append(populated_message)
        return inbox

        
    ##### UPDATE METHOD #####
    
    # Can't edit a message after it's been sent, silly goose. ;)
    
    ##### DELETE MESSAGE #####
    @classmethod
    def delete_message_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            DELETE FROM messages
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    






    # ##### VALIDATION METHODS ######
    
    # @staticmethod
    # def validate_new_post(new_post):
    #     is_valid = True
    #     if len(new_post['content']) < 1:
    #         flash("The post cannot be blank.", "post")
    #         is_valid = False
    #     return is_valid

