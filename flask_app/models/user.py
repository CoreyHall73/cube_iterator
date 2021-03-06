from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from flask_app.models.solve import Solve

DATABASE = 'cube_iteration'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.solves = []


    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all(cls) -> object or bool:
        query = "SELECT * FROM users;"
        result = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users LEFT JOIN solves ON users.id = solves.user_id WHERE users.id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return results

    @classmethod
    def get_user_with_solves( cls , data ):
        query = "SELECT * FROM users LEFT JOIN solves ON solves.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        solve = cls( results[0] )
        if not results[0]['solves.id']:
            return solve
        for row_from_db in results:
            print(row_from_db)
            solve_data = {
                "id" : row_from_db["solves.id"],
                "time" : row_from_db["time"],
                "scramble" : row_from_db["scramble"],
                "user_id" : row_from_db["user_id"],
                "created_at" : row_from_db["solves.created_at"],
                "updated_at" : row_from_db["updated_at"]
            }
            solve.solves.append( Solve( solve_data ) )
        return solve

    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True 
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid