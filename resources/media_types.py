import datetime
from flask_restful import Resource, reqparse
from models.media_types import MediaTypeModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class NewMediaType(Resource):
    @classmethod
    def post(cls):
        data = parser.parse_args()
        if MediaTypeModel.find_by_name(data['name']):
            return {'message': 'Media Type with this Name Already Existed'}, 403
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Media Type'}, 400
        
        new_mediatype = MediaTypeModel(
                name=data['name'],
                created_at=_created_at
            )
        try:
            new_mediatype.save_to_db()
            new_id = new_mediatype.mediatypeid
            return {
                        'message': 'New Media Type Has been Added',
                        'MediaTypeDetails': {
                            'id': new_id,
                            'name': data['name'],
                            'created_at': _created_at
                        }
                    }, 201
        except:
            return {
                       'message': 'Something Went Wrong'
                   }, 500


class GetAllMediaTypes(Resource):
    @classmethod
    def get(cls):
        try:
            return MediaTypeModel.return_all()
        except:
            return {
                       'message': 'Something Went Wrong'
                   }, 500


class MediaType(Resource):
    @classmethod
    def get(cls, mediatype_id: int):
        mediatype = MediaTypeModel.find_by_id(mediatype_id)
        if not mediatype:
            return {'message': 'Media Type Not Found'}, 404
        try:
            return mediatype.json(), 200
        except:
            return {
                   'message': 'Something Went Wrong'
               }, 500

    @classmethod
    def delete(cls, mediatype_id: int):
        mediatype_id = MediaTypeModel.find_by_id(mediatype_id)
        if not mediatype_id:
            return {'message': 'No Such Media Type Exist'}, 404
        try:
            mediatype_id.delete_from_db(mediatype_id)
            return {
                'message': 'Media Type has been deleted'
            }
        except:
            return {
                       'message': 'Something went Wrong'
                   }, 500


class UpdateMediaType(Resource):
    @classmethod
    def put(cls, mediatype_id):
        id = MediaTypeModel.find_by_id(mediatype_id)
        if not id:
            return {'message': 'No Such Media Type Exist'}, 404
        data = parser.parse_args()
        if MediaTypeModel.find_by_name(data['name']):
            return {'message': 'Media Type with this name already exists'}, 403
        updated_mediaType = MediaTypeModel(
            name=data['name'],
            created_at=None
        )
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Media Type'}, 400
        try:
            mediatype = MediaTypeModel.find_by_id(mediatype_id)
            mediatype.name = data['name']
            updated_mediaType.commit_db()
            return {
                       'message': 'Media Type Has been Updated',
                       'GenreDetails': {
                           'id': mediatype_id,
                           'name': data['name']
                       }
                   }, 200
        except:
            return {
                       'message': 'Something Went Wrong'
                   }, 500
