from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse
import datetime
from models.tracks import TracksModel
from models.album import AlbumModel
from models.genre import GenreModel
from models.media_types import MediaTypeModel
from models.artist import ArtistModel
from db import db
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('album_id',
                    type=int,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('mediatype_id',
                    type=int,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('genre_id',
                    type=int,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('composer',
                    type=str,
                    help='This field cannot be blank',
                    required=True)


class NewTrack(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        if not AlbumModel.find_by_id(data['album_id']):
            return {'message': 'No Such Album Exists'}, 404
        if not GenreModel.find_by_id(data['genre_id']):
            return {'message': 'No Such Genre Exists'}, 404
        if not MediaTypeModel.find_by_id(data['mediatype_id']):
            return {'message': 'No Such Media Type Exists'}, 404
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Track Name'}, 400
        if data['composer'].isspace():
            return {'message': 'Please Enter Composer Name'}, 400
        if TracksModel.find_song_already_created(data['name'], data['album_id'], data['genre_id'],
                                                 data['mediatype_id']):
            return{'message': 'Track with all this information is already Exists'}, 403
        _created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            new_track = TracksModel(
                name=data['name'],
                albumid=data['album_id'],
                mediatypeid=data['mediatype_id'],
                genreid=data['genre_id'],
                composer=data['composer'],
                created_at=_created_at
            )
            new_track.save_to_db()
            new_id = new_track.trackid
            artist_id = AlbumModel.find_by_id(data['album_id']).artist_id
            artist_name = ArtistModel.find_by_id(artist_id).name
            return {
                'message': 'New Track has been Added',
                'data': {
                    'track_id': new_id,
                    'name': data['name'],
                    'composer': data['composer'],
                    'created_at': _created_at,
                    'track_info': {
                        'artist_name': artist_name,
                        'album': AlbumModel.find_by_id(data['album_id']).title,
                        'media_type': MediaTypeModel.find_by_id(data['mediatype_id']).name,
                        'genre': GenreModel.find_by_id(data['genre_id']).name
                    }
            }
            },201
        except:
            return {
                'message': 'Something went wrong'
            }, 500


class Tracks(Resource):
    def get(self, track_id: int):
        track = TracksModel.find_by_id(track_id)
        if not track:
            return {'message': 'No Such Track Exists'}, 404
        try:
            return track.json(track_id)
        except:
            return {
                'message': 'Something went wrong'
                }, 500

    @jwt_required
    def delete(self, track_id: int):
        track_id = TracksModel.find_by_id(track_id)
        if not track_id:
            return {'message': 'No Such Track Exists'}, 404
        try:
            track_id.delete_from_db(track_id)
            return {'message': 'Track has been deleted'}
        except IntegrityError as e:
            db.session.rollback()
            return dict(message=e._message())


class GetAllTracks(Resource):
    @jwt_optional
    def get(self):
        if TracksModel.is_data_present() is None:
            return {'message': 'No Data Available.'}
        current_user = get_jwt_identity()
        if not current_user:
            return TracksModel.return_two_records()
        try:
            return TracksModel.return_all()
        except:
            return {
                'message': 'Something went wrong'
                }, 500


class UpdateTrack(Resource):
    @jwt_required
    def put(self, track_id: int):
        data = parser.parse_args()
        if not AlbumModel.find_by_id(data['album_id']):
            return {'message': 'No Such Album Exists'}, 404
        if not GenreModel.find_by_id(data['genre_id']):
            return {'message': 'No Such Genre Exists'}, 404
        if not MediaTypeModel.find_by_id(data['mediatype_id']):
            return {'message': 'No Such Media Type Exists'}, 404
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Track Name'}, 400
        if data['composer'].isspace():
            return {'message': 'Please Enter Composer Name'}, 400
        track = TracksModel.find_by_id(track_id)
        if not track:
            return {'message': 'No Such Track found.'}, 404
        if (TracksModel.find_song_already_created(data['name'],
            data['album_id'], data['genre_id'],
            data['mediatype_id']) and (data['composer'] is track.composer)):
            return {'message': 'Track with all this information is already Exists'}, 403
        try:
            track.name = data['name']
            track.albumid = data['album_id']
            track.mediatypeid = data['mediatype_id']
            track.genreid = data['genre_id']
            track.composer = data['composer']
            db.session.commit()
            artist_id = AlbumModel.find_by_id(data['album_id']).artist_id
            artist_name = ArtistModel.find_by_id(artist_id).name
            return {
                'message': 'Track has been Updated',
                'Track_Details': {
                    'track_id': track_id,
                    'name': data['name'],
                    'composer': data['composer'],
                    'created_at': track.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'track_info': {
                        'artist_name': artist_name,
                        'album': AlbumModel.find_by_id(data['album_id']).title,
                        'media_type': MediaTypeModel.find_by_id(data['mediatype_id']).name,
                        'genre': GenreModel.find_by_id(data['genre_id']).name
                    }
                }

            }, 200
        except:
            return {
                'message': 'Something went wrong'
                }, 500
