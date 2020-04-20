from db import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password,created_at):
        self.username = username
        self.password = password
        self.created_at = created_at

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'user_id': x.id,
                'username': x.username,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
