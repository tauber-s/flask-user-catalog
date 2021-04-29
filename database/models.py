from .db import db_psql
 
class User(db_psql.Model):
    id = db_psql.Column(db_psql.Integer, primary_key=True)
    first_name = db_psql.Column(db_psql.String(255))
    last_name = db_psql.Column(db_psql.String(255))
    ssn = db_psql.Column(db_psql.String(255), unique=True)
    birthday = db_psql.Column(db_psql.String(255))
    gender = db_psql.Column(db_psql.String(255))
    email = db_psql.Column(db_psql.String(255))

    def __init__(self, first_name, last_name, ssn, birthday, gender, email):
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn
        self.birthday = birthday
        self.gender = gender
        self.email = email
