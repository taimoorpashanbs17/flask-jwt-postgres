from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.artist import ArtistModel
import datetime


parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required = True)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewArtist(Resource):
    def post(self):
        data = parser.parse_args()
        if ArtistModel.find_by_name(data['name']):
            return {'message': 'Artist with this Name Already Existed'}, 403
        new_artist = ArtistModel(
            name=data['name'],
            created_at=_created_at
        )
        new_artist.save_to_db()
        new_id = new_artist.id
        return {
                   'message': 'New Artist Has been Added',
                   'ArtistDetails': {
                       'id': new_id,
                       'name': data['name'],
                       'created_at': _created_at
                   }
               }, 201


class UpdateArtist(Resource):
    def put(self, artist_id):
        id = ArtistModel.find_by_id(artist_id)
        if not id:
            return {'message': 'No Such Artist Exist'}, 404
        data = parser.parse_args()
        _date = id.created_at
        if ArtistModel.find_by_name(data['name']):
            return {'message': 'Artist with name already exists'}, 403
        updated_artist = ArtistModel(
                name=data['name'],
                created_at=_date.strftime("%Y-%m-%d %H:%M:%S")
            )
        artist = ArtistModel.find_by_id(artist_id)
        artist.name = data['name']
        updated_artist.commit_db()
        return {
           'message': 'Genre Has been Updated',
            'GenreDetails': {
            'id' : artist_id,
            'name': data['name'],
                'created_at':_date.strftime("%Y-%m-%d %H:%M:%S")
                }
            }, 200


class GetAllArtists(Resource):
    def get(self):
        return ArtistModel.return_all()


class Artist(Resource):
    @classmethod
    @jwt_required
    def get(cls, artist_id: int):
        artist = ArtistModel.find_by_id(artist_id)
        if not artist:
            return {'message': 'Artist Not Found'}, 404
        return artist.json(), 200

    @classmethod
    def delete(cls, artist_id):
        _artist_id = ArtistModel.find_by_id(artist_id)
        if not _artist_id:
            return {'message': 'No Such Artist Exist'}, 404
        try:
            _artist_id.delete_from_db(artist_id)
            return {
                'message': 'Genre has been deleted'
            }
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500