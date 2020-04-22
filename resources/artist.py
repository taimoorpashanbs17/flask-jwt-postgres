from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity, get_jwt_claims
from flask_restful import Resource, reqparse
from models.artist import ArtistModel
import datetime
from sqlalchemy.exc import IntegrityError
from db import db

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewArtist(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        if ArtistModel.find_by_name(data['name']):
            return {'message': 'Artist with this Name Already Existed'}, 403
        new_artist = ArtistModel(
            name=data['name'],
            created_at=_created_at
        )
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Artist Name'}, 400
        try:
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
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500


class UpdateArtist(Resource):
    @jwt_required
    def put(self, artist_id):
        id = ArtistModel.find_by_id(artist_id)
        if not id:
            return {'message': 'No Such Artist Exist'}, 404
        data = parser.parse_args()
        _date = id.created_at
        if ArtistModel.find_by_name(data['name']):
            return {'message': 'Artist with this name already exists'}, 403
        updated_artist = ArtistModel(
            name=data['name'],
            created_at=_date.strftime("%Y-%m-%d %H:%M:%S")
        )
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Artist Name'}, 400
        try:
            artist = ArtistModel.find_by_id(artist_id)
            artist.name = data['name']
            updated_artist.commit_db()
            return {
                       'message': 'Artist Has been Updated',
                       'ArtistDetails': {
                           'id': artist_id,
                           'name': data['name'],
                           'created_at': _date.strftime("%Y-%m-%d %H:%M:%S")
                       }
                   }, 200
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500


class GetAllArtists(Resource):
    @jwt_optional
    def get(self):
        if ArtistModel.is_data_present() is None:
            return {'message': 'No Data Available.'}
        current_user = get_jwt_identity()
        if not current_user:
            return ArtistModel.return_two_records()
        try:
            return ArtistModel.return_all()
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500


class Artist(Resource):
    def get(self, artist_id: int):
        artist = ArtistModel.find_by_id(artist_id)
        if not artist:
            return {'message': 'Artist Not Found'}, 404
        try:
            return artist.json(), 200
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500

    @jwt_required
    def delete(self, artist_id: int):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {
                       'message': 'Admin Privileges required'
                   }, 401
        artist_id = ArtistModel.find_by_id(artist_id)
        if not artist_id:
            return {'message': 'No Such Artist Exist'}, 404
        try:
            artist_id.delete_from_db(artist_id)
            return {
                'message': 'Artist has been deleted'
            }
        except IntegrityError as e:
            db.session.rollback()
            return dict(message=e._message())
