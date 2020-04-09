from db import db
import datetime
from sqlalchemy import func, outerjoin



class ArtistModel(db.Model):
    __tablename__ = 'artists'

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

    def json(self):
        return {
            'data': {
                'artist_id': self.id,
                'artist_name': self.name,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                # 'number_of_albums': AlbumModel.getCounts(self.id)
            }
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'artist_id': x.id,
                'artist_name': x.name,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        return {'Artists': list(map(lambda x: to_json(x), ArtistModel.query.all()))}