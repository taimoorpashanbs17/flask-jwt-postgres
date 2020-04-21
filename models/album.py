from db import db
import datetime
from models.artist import ArtistModel
from sqlalchemy import and_, func


class AlbumModel(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, title, artist_id, created_at):
        self.title = title
        self.artist_id = artist_id
        self.created_at = created_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_db(self):
        db.session.commit()

    def delete_from_db(self, _id):
        db.session.delete(_id)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter(func.lower(AlbumModel.title) == title.lower()).all()

    @classmethod
    def find_by_artistid(cls, _artistid):
        return cls.query.filter_by(artist_id = _artistid).first()

    @classmethod
    def find_by_id_and_title(cls, _id, title):
        return cls.query.filter(and_(AlbumModel.artist_id == _id,
                                     func.lower(AlbumModel.title) == title.lower())).first()

    def json(self, album_id):
        return {
            'data':{
                    'album_id': album_id,
                    'title': self.title,
                    'artist_name': ArtistModel.find_by_id(self.artist_id).name,
                    'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
        }

    @classmethod
    def return_all(self):
        def to_json(x):
            return {
                'data':{
                    'album_id': x.id,
                    'title': x.title,
                    'artist_name': ArtistModel.find_by_id(x.artist_id).name,
                    'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
        return {'Albums': list(map(lambda x: to_json(x), AlbumModel.query.all()))}

    @classmethod
    def return_two_records(self):
        def to_json(x):
            return {
                'data': {
                    'album_id': x.id,
                    'title': x.title,
                    'artist_name': ArtistModel.find_by_id(x.artist_id).name,
                    'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            }

        return {'Albums': list(map(lambda x: to_json(x), AlbumModel.query.limit(2).all())),
                'message': 'More Data can be display if you enter access_token.'}

    @classmethod
    def is_data_present(cls):
        return cls.query.first()
