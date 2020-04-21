from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

# import flask_login
# login_manager = flask_login.LoginManager()

from resources.user import UserRegister, User, UserLogin, TokenRefresh, \
    GetUsers, UserLogout, RevokedTokenModel
from resources.genre import Genre, UpdateGenre, NewGenre, GetAllGenres
from resources.artist import NewArtist, UpdateArtist, GetAllArtists, Artist
from resources.album import NewAlbum, EditAlbum, GetAllAlbums, Album
from resources.playlist import GetAllPlaylists, NewPlaylist, UpdatePlaylist, Playlist
from resources.media_types import GetAllMediaTypes, NewMediaType, UpdateMediaType, MediaType
from resources.tracks import NewTrack, Tracks, GetAllTracks, UpdateTrack

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Test@12345@localhost:5432/flask_restapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose'  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)
# login_manager.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


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


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description': 'The token has expired.',
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description': 'Invalid Token Entered'
    }, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'message': 'Request does not contain an access token.'
    }, 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {
        'message': 'The token is not fresh.'
    }, 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        'message': 'Your token has been revoked.'
    }, 401


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(GetUsers, '/all_users')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

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
api.add_resource(NewPlaylist, '/new_playlist')
api.add_resource(UpdatePlaylist, '/update_playlist/<playlist_id>')
api.add_resource(Playlist, '/playlist/<int:playlist_id>')

api.add_resource(NewMediaType, '/new_mediaplayer')
api.add_resource(MediaType, '/mediatype/<int:mediatype_id>')
api.add_resource(UpdateMediaType, '/update_mediatype/<mediatype_id>')
api.add_resource(GetAllMediaTypes, '/all_mediatypes')

api.add_resource(NewTrack, '/new_track')
api.add_resource(Tracks, '/track/<int:track_id>')
api.add_resource(GetAllTracks, '/all_tracks')
api.add_resource(UpdateTrack, '/update_track/<int:track_id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)