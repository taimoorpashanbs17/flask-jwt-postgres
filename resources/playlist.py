import datetime

from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.playlist import PlaylistModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)


class GetAllPlaylists(Resource):
    @jwt_optional
    def get(self):
        if PlaylistModel.is_data_present() is None:
            return {'message': 'No Data Available.'}
        current_user = get_jwt_identity()
        if not current_user:
            return PlaylistModel.return_two_records()
        return PlaylistModel.return_all()


class NewPlaylist(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        if PlaylistModel.find_by_name(data['name']):
            return {'message': 'Playlist with this Name Already Existed'}, 403
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Playlist Name'}, 400
        created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            new_playlist = PlaylistModel(
                    name=data['name'],
                    created_at=created_at
                )
            new_playlist.save_to_db()
            new_id = new_playlist.id
            return {
                    'message': 'New Playlist Has been Added',
                    'PlaylistDetails': {
                        'id': new_id,
                        'name': data['name'],
                        'created_at': created_at
                               }
                           }, 201
        except:
            return {
                'message': 'Something went wrong'
            }, 500


class UpdatePlaylist(Resource):
    @jwt_required
    def put(self, playlist_id):
        id = PlaylistModel.find_by_id(playlist_id)
        if not id:
            return {'message': 'No Such Playlist Exist'}, 404
        data = parser.parse_args()
        if PlaylistModel.find_by_name(data['name']):
            return {'message': 'Playlist with this name already exists'}, 403
        updated_genre = PlaylistModel(
            name=data['name'],
            created_at=None
        )
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Playlist Name'}, 400
        try:
            playlist = PlaylistModel.find_by_id(playlist_id)
            playlist.name = data['name']
            updated_genre.commit_db()
            return {
                       'message': 'Playlist Has been Updated',
                       'PlaylistDetails': {
                           'id': playlist_id,
                           'name': data['name']
                       }
                   }, 200
        except:
            return {
                       'message': 'Something Went Wrong'
                   }, 500


class Playlist(Resource):
    def get(self, playlist_id: int):
        playlist = PlaylistModel.find_by_id(playlist_id)
        if not playlist:
            return {'message': 'Playlist Not Found'}, 404
        try:
            return playlist.json(), 200
        except:
            return {
                   'message': 'Something Went Wrong'
               }, 500

    @jwt_required
    def delete(self, playlist_id: int):
        playlist_id = PlaylistModel.find_by_id(playlist_id)
        if not playlist_id:
            return {'message': 'No Such Playlist Exist'}, 404
        try:
            playlist_id.delete_from_db(playlist_id)
            return {
                    'message': 'Playlist has been deleted'
                }
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500



