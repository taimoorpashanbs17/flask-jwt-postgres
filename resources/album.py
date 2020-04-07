from flask_restful import Resource, reqparse
from models.artist import ArtistModel
from models.album import AlbumModel
import datetime


parser = reqparse.RequestParser()
parser.add_argument('title',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('artist_id',
                    type=str,
                    help='This Field Cannot be blank',
                    required='True')
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewAlbum(Resource):
    def post(self):
        data = parser.parse_args()
        if AlbumModel.find_by_title(data['title']):
            return {'message': 'Album with this Name Already Existed'}, 403
        artist = ArtistModel.find_by_id(data['artist_id'])
        if not artist:
            return {'message': 'Artist Not Found'}, 404
        new_album = AlbumModel(
            title=data['title'],
            artist_id=data['artist_id'],
            created_at=_created_at
        )
        new_album.save_to_db()
        new_id = new_album.id
        return {
                   'message': 'New Album Has been Added',
                   'AlbumDetails': {
                       'id': new_id,
                       'title': data['title'],
                       'created_at': _created_at,
                       'artist_info':{
                           'artist_id': artist.id,
                           'artist_name': artist.name
                       }
                   }
               }, 201


class EditAlbum(Resource):
    def put(self, album_id):
        _albumid = AlbumModel.find_by_id(album_id)
        if not _albumid:
            return {'message': 'No Such Album Exist'}, 404
        data = parser.parse_args()
        _date = _albumid.id
        if AlbumModel.find_by_title(data['title']):
            return {'message': 'Album with this name already exists'}, 403
        _artistid = ArtistModel.find_by_id(data['artist_id'])
        if ArtistModel.find_by_id(data['artist_id']) is None:
            return {'message': 'Artist with this ID does not exists'}, 403
        updated_album = AlbumModel(
            title=data['title'],
            artist_id=data['artist_id'],
            created_at=None
        )
        album = AlbumModel.find_by_id(album_id)
        album.name = data['title']
        updated_album.commit_db()
        return {
                   'message': 'Genre Has been Updated',
                   'GenreDetails': {
                       'id': album_id,
                       'title': data['title'],
                       'created_at': _albumid.created_at.strftime("%Y-%m-%d %H:%M:%S")
                       # 'artist_info': {
                       #     'artist_id': _artistid.id,
                       #     'artist_name': _artistid.name
                       # }
                   }
               }, 200

