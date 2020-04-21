from db import db
import datetime
from sqlalchemy import func


class GenreModel(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_db(self):
        db.session.commit()

    def delete_from_db(self, id):
        db.session.delete(id)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(func.lower(GenreModel.name) == name.lower()).all()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'genre_id': x.id,
                'genre_name': x.name,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        return {'Genres': list(map(lambda x: to_json(x), GenreModel.query.all()))}

    def json(self):
        return {
            'data': {
                'genre_id': self.id,
                'genre_name': self.name,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    @classmethod
    def return_two_records(cls):
        def to_json(x):
            return {
                'genre_id': x.id,
                'genre_name': x.name,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        return {'Genres': list(map(lambda x: to_json(x), GenreModel.query.limit(2).all())),
                'message': 'More Data can be display if you enter access_token.'}

    @classmethod
    def is_data_present(cls):
        return cls.query.first()