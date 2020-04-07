from db import db
import datetime
from models.artist import ArtistModel


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

    def delete_from_db(self, id):
        db.session.delete(id)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, _title):
        return cls.query.filter_by(title=_title).first()

    def json(self, artist_id):
        return {
            'data': {
                'album_id': self.id,
                'artist_name': self.title,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'artist_info':{
                    ArtistModel.json(artist_id)
                }
            }
        }
