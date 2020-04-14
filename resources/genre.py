import datetime
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.genre import GenreModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewGenre(Resource):
    def post(self):
        data = parser.parse_args()
        if GenreModel.find_by_name(data['name']):
            return {'message': 'Genre with this Name Already Existed'}, 403
        new_genre = GenreModel(
            name=data['name'],
            created_at= _created_at
        )
        if not data['name']:
            return{'message': 'Please Enter Genre Name'}, 403
        new_genre.save_to_db()
        new_id = new_genre.id
        return{
                'message': 'New Genre Has been Added',
                'GenreDetails': {
                    'id': new_id,
                    'name': data['name'],
                    'created_at': _created_at
                }
            }, 201


class GetAllGenres(Resource):
    @classmethod
    def get(cls):
        return GenreModel.return_all()


class Genre(Resource):
    @classmethod
    def get(cls, genre_id: int):
        genre = GenreModel.find_by_id(genre_id)
        if not genre:
            return {'message': 'Genre Not Found'}, 404
        return genre.json(), 200

    @classmethod
    def delete(cls, genre_id):
        genre_id = GenreModel.find_by_id(genre_id)
        if not genre_id:
            return {'message': 'No Such Genre Exist'}, 404
        try:
            genre_id.delete_from_db(genre_id)
            return {
                'message': 'Genre has been deleted'
            }
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500


class UpdateGenre(Resource):
    def put(self, genre_id):
        id = GenreModel.find_by_id(genre_id)
        if not id:
            return {'message': 'No Such Genre Exist'}, 404
        data = parser.parse_args()
        if GenreModel.find_by_name(data['name']):
            return {'message': 'Genre with this name already exists'}, 403
        updated_genre = GenreModel(
                name=data['name'],
                created_at=None
            )
        if not data['name']:
            return{'message': 'Please Enter Genre Name'}, 403
        genre = GenreModel.find_by_id(genre_id)
        genre.name = data['name']
        updated_genre.commit_db()
        return {
           'message': 'Genre Has been Updated',
            'GenreDetails': {
            'id' : genre_id,
            'name': data['name']
                }
            }, 200




