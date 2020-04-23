from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os
from resources.user import UserRegister, User, UserLogin, TokenRefresh, \
    GetUsers, UserLogout, RevokedTokenModel, MakeInActive, UpdateUser
from resources.genre import Genre, UpdateGenre, NewGenre, GetAllGenres
from resources.artist import NewArtist, UpdateArtist, GetAllArtists, Artist
from resources.album import NewAlbum, EditAlbum, GetAllAlbums, Album
from resources.playlist import GetAllPlaylists, NewPlaylist, UpdatePlaylist, Playlist
from resources.media_types import GetAllMediaTypes, NewMediaType, UpdateMediaType, MediaType
from resources.tracks import NewTrack, Tracks, GetAllTracks, UpdateTrack

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose'
api = Api(app)
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == "admin@flask-restapi-postgres.com":
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
# api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
# api.add_resource(GetUsers, '/all_users')
api.add_resource(UpdateUser, '/update_user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(MakeInActive, '/make_inactive/<int:user_id>')

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
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)