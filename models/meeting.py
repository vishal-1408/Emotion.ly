from db import db
from datetime import datetime


class MeetingModel(db.Model):
    __tablename__='meeting'
    id = db.Column(db.Integer,primary_key=True)
    channel = db.Column(db.String(30),unique = True,nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('UserModel')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self,channel,created_by):
        self.channel = channel
        self.created_by = created_by

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetchByChannel(cls,channel):
        print("came2")
        return cls.query.filter_by(channel=channel).first()

    @classmethod
    def fetchById(cls,id):
        return cls.query.filter_by(id=id).first()



