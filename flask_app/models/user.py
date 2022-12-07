from operator import truediv
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# modeling the class after the users table from users_schema database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pwd = data['pwd']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # Class method to Create
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , pwd ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(pwd)s );"
        result  = connectToMySQL('belt_exam_schema').query_db( query, data )
        return result
    
    # Class method to Retrieve (all)
    @classmethod
    def get_all(cls):        
        query = "SELECT * FROM users;"
        results = connectToMySQL('belt_exam_schema').query_db(query)
        users = []        
        for user in results:
            users.append( cls(user) )
        return users
    
    # Class method to Retrieve user by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('belt_exam_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL('belt_exam_schema').query_db(query,data)
        return cls(result[0])
        
    
    # Static method to validate user registration
    @staticmethod
    def user_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('belt_exam_schema').query_db(query, user)
        if len(result) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user["first_name"]) <= 0:
            is_valid = False
            flash("First name is required.", "register")
        if len(user["last_name"]) <= 0:
            is_valid = False
            flash("Last name is required.", "register")
        if len(user["pwd"]) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.", "register")
        if user['pwd'] != user['confirm_pwd']:
            flash("Passwords do not match!", "register")
        return is_valid