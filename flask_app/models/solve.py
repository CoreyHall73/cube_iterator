from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from random import choices

DATABASE = 'cube_iteration'

class Solve:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.time = data['time']
        self.scramble = data['scramble']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO solves (time, user_id) VALUES (%(time)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def scramble(cls):
        moves = ["F", "F'", "F2", "U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2", "B", "B'", "B2"]
        return choices(moves, k=12)

    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM solves WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

