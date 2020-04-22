import re
from db import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(80))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    is_active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, password, first_name, last_name, is_active, created_at):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.created_at = created_at

    def json(self):
        return {
            'id': self.id,
            'email': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'user_id': x.id,
                'user_email': x.username,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'is_active': x.is_active,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def is_email_valid(cls, email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return bool(re.search(regex, email))

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
