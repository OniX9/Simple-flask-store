from db import db

class UserModel(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    email = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    