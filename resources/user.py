from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity, \
    jwt_required, get_raw_jwt, get_jti, get_jwt_claims
from models.user import UserModel, RevokedTokenModel
import datetime
from db import db
from models.user_session import UserSessionModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str
                          )
_user_parser.add_argument('password',
                          type=str
                          )
_user_parser.add_argument('first_name',
                          type=str
                          )
_user_parser.add_argument('last_name',
                          type=str
                          )
_user_parser.add_argument('is_active',
                          type= bool)
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        email_address = data['email']
        password = data['password']
        user_first_name = data['first_name']
        user_last_name = data['last_name']
        if UserModel.find_by_email(email_address):
            return {"message": "A user with that email already exists"}, 400
        if not email_address or email_address.isspace():
            return{'message': 'Please Enter email address'}, 400
        if not password or password.isspace():
            return{'message': 'Please Enter Password'}, 400
        if not user_first_name or user_first_name.isspace():
            return{'message': 'Please Enter First Name'}, 400
        if not user_last_name or user_last_name.isspace():
            return{'message': 'Please Enter Last Name'}, 400
        if UserModel.is_email_valid(email_address) is False:
            return{'message': 'Please Enter Valid email Address'},400
        _created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        new_user = UserModel(
            email=email_address,
            password=UserModel.generate_hash(password),
            first_name=user_first_name,
            last_name=user_last_name,
            is_active=True,
            created_at=_created_at
        )
        new_user.save_to_db()
        user_info = UserModel.find_by_email(email_address)
        return {'message': 'User created successfully.',
                'Data': {
                    'user_id':user_info.id,
                    'email_address': email_address,
                    'first_name': user_first_name,
                    'last_name': user_last_name,
                    'is_active': user_info.is_active,
                    'created_at': user_info.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        email_address = data['email']
        password = data['password']
        current_user = UserModel.find_by_email(email_address)
        # user_full_name = current_user.first_name+" "+current_user.last_name
        current_user_id = UserModel.find_by_email(email_address).id
        user_session_info = UserSessionModel.find_by_id_and_time_out(current_user_id)
        if user_session_info:
            return {'message': 'You are Already Login'}, 400
        if UserModel.is_email_valid(email_address) is False:
            return{'message': 'Please Enter Valid email Address'},400
        if not email_address or email_address.isspace():
            return{'message': 'Please Enter email address'}, 400
        if not password or password.isspace():
            return{'message': 'Please Enter Password'}, 400
        if user_session_info:
            return {'message': 'You are Already Login'}, 400
        user_time_in = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if not current_user:
            return {'message': 'User doesn\'t exist'}, 401
        if UserModel.verify_hash(password, current_user.password):
            access_token = create_access_token(identity=email_address, fresh=True)
            refresh_token = create_refresh_token(identity=email_address)
            user_id = UserModel.find_by_email(email_address).id
            new_session = UserSessionModel(
                user_id=user_id,
                session_time_in=user_time_in,
                session_time_out=None
            )
            new_session.save_to_db()
            return {
                       'message': 'User have logged in',
                        'session_time_in': user_time_in,
                       'access_token': access_token,
                        'refresh_token': refresh_token
                   }, 200

        else:

            return {'message': 'Wrong credentials'}, 401


class GetUsers(Resource):
    @classmethod
    def get(cls):
        return UserModel.return_all()


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        try:
            jti = get_raw_jwt()['jti']
            email_address = get_jwt_identity()
            user_info = UserModel.find_by_email(email_address)
            session_id = UserSessionModel.find_by_id_and_time_out(user_info.id).session_id
            time_out = UserSessionModel.find_by_session_id(session_id)
            time_out.session_time_out = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            db.session.commit()
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            session_info = UserSessionModel.find_by_user_id(user_info.id)
            return {
                'message': 'User Logged out',
                'user_Details': {
                    'email_address': email_address,
                    'first_name': user_info.first_name,
                    'last_name': user_info.last_name,
                    'time_in': session_info.session_time_in.strftime('%Y-%m-%d %H:%M:%S'),
                    'time_out': session_info.session_time_out.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        except AttributeError:
            return {'message': 'You are not logged in, Kindly Logged in'}, 401


class MakeInActive(Resource):
    @jwt_required
    def post(self, user_id: int):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {
                'message': 'Admin Previligies required'
            }, 401
        user_info = UserModel.find_by_id(user_id)
        if not user_info:
            return {'message': 'User Does not exists'}, 400
        user_full_name = user_info.first_name + " " + user_info.last_name
        data = _user_parser.parse_args()
        user_info.is_active = data['is_active']
        db.session.commit()
        if user_info.is_active is False:
            return {
                'message': user_full_name+' is now not an Active'
            }
        return {
            'message': user_full_name+' is now Active'
        }, 200


class UpdateUser(Resource):
    @jwt_required
    def put(self, user_id: int):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {
                       'message': 'Admin Previligies required'
                   }, 401
        user_info = UserModel.find_by_id(user_id)
        if not user_info:
            return {'message': 'User Does not exists'}, 400
        data = _user_parser.parse_args()
        user_first_name = data['first_name']
        user_last_name = data['last_name']
        if not user_first_name or user_first_name.isspace():
            return{'message': 'Please Enter First Name'}, 400
        if not user_last_name or user_last_name.isspace():
            return{'message': 'Please Enter Last Name'}, 400
        user_info.first_name = user_first_name
        user_info.last_name = user_last_name
        db.session.commit()
        return {
            'message': 'User Info has been Updated',
            'Data':{
                'user_id': user_info.id,
                'email_address': user_info.email,
                'first_name': user_info.first_name,
                'last_name': user_info.last_name,
                'is_active': user_info.is_active,
                'created_at': user_info.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }