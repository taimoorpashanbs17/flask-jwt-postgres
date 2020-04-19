from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
import datetime
from models.tracks import TracksModel
from models.album import AlbumModel
from models.genre import GenreModel
from models.media_types import MediaTypeModel
from models.artist import ArtistModel
from db import db

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
parser.add_argument('milliseconds',
                    type=int,
                    help='Milliseconds field cannot be left blank',
                    required=True)
parser.add_argument('bytes',
                    type=int,
                    help='Bytes field cannot be left blank',
                    required=True)
parser.add_argument('unit_price',
                    type=int,
                    help='Unit Price field cannot be left blank',
                    required=True)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
        new_track = TracksModel(
            name=data['name'],
            albumid=data['album_id'],
            mediatypeid=data['mediatype_id'],
            genreid=data['genre_id'],
            composer=data['composer'],
            milli_seconds=data['milliseconds'],
            bytes=data['bytes'],
            unitprice=data['unit_price'],
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
                'milli_seconds': data['milliseconds'],
                'bytes': data['bytes'],
                'unit_price': data['unit_price'],
                'created_at': _created_at,
                'track_info': {
                    'artist_name': artist_name,
                    'album': AlbumModel.find_by_id(data['album_id']).title,
                    'media_type': MediaTypeModel.find_by_id(data['mediatype_id']).name,
                    'genre': GenreModel.find_by_id(data['genre_id']).name
                }
        }
        },201


class Tracks(Resource):
    def get(self, track_id: int):
        track = TracksModel.find_by_id(track_id)
        if not track:
            return {'message': 'No Such Track Exists'}, 404
        return track.json(track_id)

    def delete(self, track_id: int):
        track_id = TracksModel.find_by_id(track_id)
        if not track_id:
            return {'message': 'No Such Track Exists'}, 404
        track_id.delete_from_db(track_id)
        return {'message': 'Track has been deleted'}


class GetAllTracks(Resource):
    def get(self):
        return TracksModel.return_all()


class UpdateTrack(Resource):
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
        track.name = data['name']
        track.albumid = data['album_id']
        track.mediatypeid = data['mediatype_id']
        track.genreid = data['genre_id']
        track.composer = data['composer']
        track.milli_seconds = data['milliseconds']
        track.bytes = data['bytes']
        track.unitprice = data['unit_price']
        db.session.commit()
        artist_id = AlbumModel.find_by_id(data['album_id']).artist_id
        artist_name = ArtistModel.find_by_id(artist_id).name
        return {
            'message': 'Track has been Updated',
            'Track_Details': {
                'track_id': track_id,
                'name': data['name'],
                'composer': data['composer'],
                'milli_seconds': data['milliseconds'],
                'bytes': data['bytes'],
                'unit_price': data['unit_price'],
                'created_at': track.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'track_info': {
                    'artist_name': artist_name,
                    'album': AlbumModel.find_by_id(data['album_id']).title,
                    'media_type': MediaTypeModel.find_by_id(data['mediatype_id']).name,
                    'genre': GenreModel.find_by_id(data['genre_id']).name
                }
            }

        }
