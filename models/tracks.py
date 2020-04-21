from db import db
import datetime
from resources.album import AlbumModel
from resources.media_types import MediaTypeModel
from resources.genre import GenreModel
from resources.artist import ArtistModel
from sqlalchemy import and_, func


class TracksModel(db.Model):
    __tablename__ = 'tracks'
    trackid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    albumid = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    mediatypeid = db.Column(db.Integer, db.ForeignKey('media_types.mediatypeid'), nullable=False)
    genreid = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    composer = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, albumid, mediatypeid, genreid,
                 composer, created_at):
        self.name = name
        self.albumid = albumid
        self.mediatypeid = mediatypeid
        self.genreid = genreid
        self.composer = composer,
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
    def find_by_id(cls, id):
        return cls.query.filter_by(trackid=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(func.lower(TracksModel.name) == name.lower()).all()

    @classmethod
    def find_by_albumid(cls, album_id):
        return cls.query.filter_by(albumid=album_id).first()

    @classmethod
    def find_by_mediatypeid(cls, mediatype_id):
        return cls.query.filter_by(mediatypeid=mediatype_id).first()

    @classmethod
    def find_by_genreid(cls, genre_id):
        return cls.query.filter_by(genreid=genre_id).first()

    @classmethod
    def find_song_already_created(cls, name, album_id, genre_id, mediatype_id):
        return cls.query.filter(and_(TracksModel.albumid == album_id,
                                     func.lower(TracksModel.name) == name.lower()),
                                genre_id == TracksModel.genreid,
                                TracksModel.mediatypeid == mediatype_id).first()

    @classmethod
    def get_artistname(cls, album_id):
        artistid = AlbumModel.find_by_id(album_id).artist_id
        artist_name = ArtistModel.find_by_id(artistid).name
        return artist_name

    def json(self, track_id):
        return {
            'data': {
                'track_id': track_id,
                'name': self.name,
                'composer': self.composer,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'track_info': {
                    'artist_name': TracksModel.get_artistname(self.albumid),
                    'album': AlbumModel.find_by_id(self.albumid).title,
                    'genre': GenreModel.find_by_id(self.genreid).name,
                    'media_type': MediaTypeModel.find_by_id(self.mediatypeid).name
                }
            }
        }

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'track_id': x.trackid,
                'name': x.name,
                'composer': x.composer,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'track_info': {
                    'artist_name': TracksModel.get_artistname(x.albumid),
                    'album': AlbumModel.find_by_id(x.albumid).title,
                    'genre': GenreModel.find_by_id(x.genreid).name,
                    'media_type': MediaTypeModel.find_by_id(x.mediatypeid).name
                }
            }

        return {'Tracks': list(map(lambda x: to_json(x), TracksModel.query.all()))}

    @classmethod
    def return_two_records(cls):
        def to_json(x):
            return {
                'track_id': x.trackid,
                'name': x.name,
                'composer': x.composer,
                'created_at': x.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'track_info': {
                    'artist_name': TracksModel.get_artistname(x.albumid),
                    'album': AlbumModel.find_by_id(x.albumid).title,
                    'genre': GenreModel.find_by_id(x.genreid).name,
                    'media_type': MediaTypeModel.find_by_id(x.mediatypeid).name
                }
            }

        return {'Tracks': list(map(lambda x: to_json(x), TracksModel.query.limit(2).all())),
                'message': 'More Data can be display if you enter access_token.'}

    @classmethod
    def is_data_present(cls):
        return cls.query.first()
