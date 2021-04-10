from db import db
from datetime import datetime


class ParticipantModel(db.Model):
    __tablename__='participants'
    id = db.Column(db.Integer,primary_key=True)
    token = db.Column(db.String(150),nullable=False)
    mid = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    happy= db.Column(db.Integer,default=0)
    disgust= db.Column(db.Integer,default=0)
    surprise= db.Column(db.Integer,default=0)
    fear= db.Column(db.Integer,default=0)
    angry= db.Column(db.Integer,default=0)
    neutral= db.Column(db.Integer,default=0)
    sad= db.Column(db.Integer,default=0)
    muid = db.Column(db.Integer)
    max= db.Column(db.String(9),default='')

    def __init__(self,token,mid,uid):
        self.token = token
        self.mid = mid
        self.uid = uid

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetchByUid(cls,uid):
        return cls.query.filter_by(uid=uid).first()

    @classmethod
    def fetchById(cls,id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def fetchByMUid(cls,id):
        id =int(id)
        return cls.query.filter_by(muid=id).first()


    @classmethod
    def fetchByMid(cls,mid):
        return cls.query.filter_by(mid=mid).first()
    @classmethod
    def fetchByMidAndUid(cls,mid,uid):
        return cls.query.filter_by(mid=mid,uid=uid).first()




