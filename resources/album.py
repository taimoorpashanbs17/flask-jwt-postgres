from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse
from models.artist import ArtistModel
from models.album import AlbumModel
import datetime
from db import db
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()
parser.add_argument('title',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('artist_id',
                    type=int,
                    help='This Field Cannot be blank',
                    required='True')
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewAlbum(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        _album_artist = AlbumModel.find_by_id_and_title(data['artist_id'],
                                                        data['title'])
        if _album_artist:
            return {'message': 'Album with this artist already exists'}, 403
        artist = ArtistModel.find_by_id(data['artist_id'])
        if not artist:
            return {'message': 'No Such Artist Exists'}, 404
        if not data['title'] or data['title'].isspace():
            return {'message': 'Please Enter Album Name'}, 400
        new_album = AlbumModel(
            title=data['title'],
            artist_id=data['artist_id'],
            created_at=_created_at
        )
        try:
            new_album.save_to_db()
            new_id = new_album.id
            return {
                'message': 'New Album Has been Added',
                'AlbumDetails': {
                    'id': new_id,
                    'title': data['title'],
                    'created_at': _created_at,
                    'artist_name': artist.name
                 }
            }, 201
        except:
            return {
                'message': 'Something Went Wrong'
                   }, 500


class EditAlbum(Resource):
    @jwt_required
    def put(self, album_id):
        data = parser.parse_args()
        _album_id = AlbumModel.find_by_id(album_id)
        _artist_id = ArtistModel.find_by_id(data['artist_id'])
        _album_name = AlbumModel.find_by_title(data['title'])
        _album_artist = AlbumModel.find_by_id_and_title(data['artist_id'],
                                                        data['title'])
        if not _album_id:
            return {'message': 'No Such Album Exist'}, 404
        if _artist_id is None:
            return {'message': 'Artist with this ID does not exists'}, 404
        if _album_artist:
            return {'message': 'Album with this artist already exists'}, 403
        if not data['title'] or data['title'].isspace():
            return {'message': 'Please Enter Album Name'}, 400
        album = AlbumModel.find_by_id(album_id)
        album.title = data['title']
        album.artist_id = data['artist_id']
        artist = ArtistModel.find_by_id(data['artist_id'])
        db.session.commit()
        return {
                   'message': 'Genre Has been Updated',
                   'GenreDetails': {
                       'id': album_id,
                       'title': data['title'],
                       'created_at': album.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                       'artist_name': artist.name
                   }
               }, 200


class GetAllAlbums(Resource):
    @jwt_optional
    def get(self):
        if AlbumModel.is_data_present() is None:
            return {'message': 'No Data Available.'}, 200
        current_user = get_jwt_identity()
        if not current_user:
            return AlbumModel.return_two_records()
        try:
            return AlbumModel.return_all()
        except:
            return {'message': 'Something went wrong'}, 500


class Album(Resource):
    def get(self, album_id: int):
        _album_id = AlbumModel.find_by_id(album_id)
        if not _album_id:
            return {'message': 'No Such Album Exist'}, 404
        try:
            return _album_id.json(album_id)
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500

    @jwt_required
    def delete(self, album_id: int):
        album_id = AlbumModel.find_by_id(album_id)
        if not album_id:
            return {'message': 'No Such Album Exist'}, 404
        try:
            album_id.delete_from_db(album_id)
            return {
                'message': 'Album has been deleted'
            }
        except IntegrityError as e:
            db.session.rollback()
            return dict(message=e._message())
