from db import db
from datetime import datetime
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

bcrypt = Bcrypt()



class UserModel(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique = True)
    password = db.Column(db.String(150),nullable=False)
    name=db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(200),nullable=False)

    def __init__(self,email,name=None,password=None):
        self.email = email
        self.name = name
        self.avatar = os.environ.get('AVATAR_DEFAULT')
        self.password = bcrypt.generate_password_hash(password) if password else password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetchByEmail(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetchById(cls,id):
        return cls.query.filter_by(id=id).first()
    
    @staticmethod
    def checkPassword(hashedP,password):
        return bcrypt.check_password_hash(hashedP,password)
    


