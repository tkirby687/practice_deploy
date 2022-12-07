from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Show():
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        
    @classmethod
    def create_show(cls, form_data):
        query = "INSERT INTO shows (title, description, release_date, user_id) VALUES (%(title)s, %(description)s, %(release_date)s, %(user_id)s);"
        return connectToMySQL('belt_exam_schema').query_db(query, form_data)
    
    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows;"
        return connectToMySQL('belt_exam_schema').query_db(query)
    
    @classmethod
    def get_all_shows_with_user(cls):
        query = "SELECT * FROM shows LEFT JOIN users on shows.user_id = users.id;"
        shows = connectToMySQL('belt_exam_schema').query_db(query)
        results = []
        for show in shows:
            data = {
                'id' : show['users.id'],
                'first_name' : show['first_name'],
                'last_name' : show['last_name'],
                'email' : show['email'],
                'pwd' : show['pwd'],
                'created_at' : show['users.created_at'],
                'updated_at' : show['users.updated_at']
            }
            one_show = cls(show)
            one_show.creator = user.User(data)
            results.append(one_show) 
        return shows
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL('belt_exam_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_show(cls, form_data):
        query = "UPDATE shows SET title=%(title)s, description=%(description)s, release_date=%(release_date)s WHERE id=%(id)s;"
        return connectToMySQL('belt_exam_schema').query_db(query, form_data)
    
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id=%(id)s;"
        return connectToMySQL('belt_exam_schema').query_db(query, data)
    
    @staticmethod
    def show_validator(data):
        is_valid = True
        if len(data["title"]) <= 0:
            is_valid = False
            flash("Title is required.")        
        query = "SELECT * FROM shows WHERE title = %(title)s;"
        result = connectToMySQL('belt_exam_schema').query_db(query, data)
        if len(result) >= 1:
            flash("Show already exists.")
            is_valid = False   
        if len(data["description"]) <= 0:
            is_valid = False
            flash("Description is required.")
        if data['release_date'] == '':
            is_valid = False
            flash("Release date is required.")
        return is_valid