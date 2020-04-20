from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity, \
    jwt_required, get_raw_jwt
from models.user import UserModel, RevokedTokenModel
import datetime
from db import db
from models.user_session import UserSessionModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            created_at=_created_at
        )
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

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
        current_user = UserModel.find_by_username(data['username'])
        user_id = UserModel.find_by_username(data['username']).id
        user_time_in = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 401
        user_login = UserSessionModel.find_by_id_and_time_out(user_id)
        if user_login:
            return {
                'message': 'User Already logged in'
            }, 401
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            user_id = UserModel.find_by_username(data['username']).id
            new_session = UserSessionModel(
                user_id=user_id,
                session_time_in=user_time_in,
                session_time_out=None
            )
            new_session.save_to_db()
            return {
                       'message': 'Logged in as {}'.format(current_user.username),
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
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.

        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        username = get_jwt_identity()
        user_id = UserModel.find_by_username(username).id
        session_id = UserSessionModel.find_by_id_and_time_out(user_id).session_id
        time_out = UserSessionModel.find_by_session_id(session_id)
        time_out.session_time_out = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.commit()
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        session_info = UserSessionModel.find_by_user_id(user_id)
        return {
            'message': 'User Logged out',
            'user_Details': {
                'user_name': username,
                'time_in': session_info.session_time_in.strftime('%Y-%m-%d %H:%M:%S'),
                'time_out': session_info.session_time_out.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
