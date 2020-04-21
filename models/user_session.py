from db import db
import datetime
from sqlalchemy import and_


class UserSessionModel(db.Model):
    __tablename__ = 'user_session'
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_time_in = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    session_time_out = db.Column(db.DateTime)

    def __init__(self, user_id, session_time_in, session_time_out):
        self.user_id = user_id
        self.session_time_in = session_time_in
        self.session_time_out = session_time_out

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_db(self):
        db.session.commit()

    @classmethod
    def find_by_session_id(cls, session_id):
        return cls.query.filter_by(session_id=session_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_id_and_time_out(cls, userid):
        return cls.query.filter(and_(UserSessionModel.user_id == userid,
                                     UserSessionModel.session_time_out == None)).first()

    @classmethod
    def find_by_time_in(cls, session_time_out):
        return cls.query.filter_by(session_time_in=session_time_out).first()


