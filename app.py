import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


from resources.user import UserRegister, User, UserLogin, TokenRefresh, GetUsers
from resources.genre import Genre, UpdateGenre, NewGenre, GetAllGenres
from resources.artist import NewArtist, UpdateArtist, GetAllArtists, Artist
from resources.album import NewAlbum, EditAlbum, GetAllAlbums, Album
from resources.playlist import GetAllPlaylists

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'jdbc:postgresql://ec2-54-197-48-79.'
                                                       'compute-1.amazonaws.com:5432/d3f3hie47pgpb0')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)

jwt = JWTManager(app)

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below.
"""
@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(GetUsers, '/all_users')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(NewGenre, '/new_genre')
api.add_resource(Genre, '/genre/<int:genre_id>')
api.add_resource(UpdateGenre, '/update_genre/<genre_id>')
api.add_resource(GetAllGenres, '/all_genre')

api.add_resource(NewArtist, '/new_artist')
api.add_resource(UpdateArtist, '/update_artist/<artist_id>')
api.add_resource(GetAllArtists, '/all_artist')
api.add_resource(Artist, '/artist/<artist_id>')

api.add_resource(NewAlbum, '/new_album')
api.add_resource(EditAlbum, '/update_album/<album_id>')
api.add_resource(GetAllAlbums, '/all_albums')
api.add_resource(Album, '/album/<int:album_id>')

api.add_resource(GetAllPlaylists, '/all_playlists')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(port=5000)