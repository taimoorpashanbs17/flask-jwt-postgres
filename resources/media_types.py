import datetime
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse
from models.media_types import MediaTypeModel
from sqlalchemy.exc import IntegrityError
from db import db

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)


class NewMediaType(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        if MediaTypeModel.find_by_name(data['name']):
            return {'message': 'Media Type with this Name Already Existed'}, 403
        if not data['name'] or data['name'].isspace():
            return {'message': 'Please Enter Media Type'}, 400
        _created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        new_media_type = MediaTypeModel(
                name=data['name'],
                created_at=_created_at
            )
        try:
            new_media_type.save_to_db()
            new_id = new_media_type.mediatypeid
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
    @jwt_optional
    def get(self):
        if MediaTypeModel.is_data_present() is None:
            return {'message': 'No Data Available.'}
        current_user = get_jwt_identity()
        if not current_user:
            return MediaTypeModel.return_two_records()
        try:
            return MediaTypeModel.return_all()
        except:
            return {
                       'message': 'Something Went Wrong'
                   }, 500


class MediaType(Resource):
    def get(self, media_type_id: int):
        media_type = MediaTypeModel.find_by_id(media_type_id)
        if not media_type:
            return {'message': 'Media Type Not Found'}, 404
        try:
            return media_type.json(), 200
        except:
            return {
                   'message': 'Something Went Wrong'
               }, 500

    @jwt_required
    def delete(self, mediatype_id: int):
        mediatype_id = MediaTypeModel.find_by_id(mediatype_id)
        if not mediatype_id:
            return {'message': 'No Such Media Type Exist'}, 404
        try:
            mediatype_id.delete_from_db(mediatype_id)
            return {
                    'message': 'Media Type has been deleted'
                }
        except IntegrityError as e:
            db.session.rollback()
            return dict(message=e._message())


class UpdateMediaType(Resource):
    @jwt_required
    def put(self, mediatype_id):
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
