from flask_restful import Resource, reqparse
from models.playlist import PlaylistModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    type=str,
                    help='This field cannot be blank',
                    required=True)


class GetAllPlaylists(Resource):
    def get(self):
        return PlaylistModel.return_all()