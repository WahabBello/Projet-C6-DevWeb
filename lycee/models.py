from datetime import datetime
from lycee import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.orm import validates

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(20), nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number= db.Column(db.String(250), unique=True, nullable=False)
    niveau= db.Column(db.String(250), nullable=False)
    classe= db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return f"User('{self.prenom}', '{self.nom}','{self.email}','{self.number}')"

    @validates('classe')
    def convert_upper(self, key,value):
        return value.upper()

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)

    
    def __repr__(self):
        return f"('{self.title}')"

    @validates('title')
    def convert_upper(self, key,value):
        return value.upper()
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}','{self.password}')"

'''     '''