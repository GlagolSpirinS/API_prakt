from flask_restful import Resource, reqparse
from models import Playlist, AudioRecord
from extensions import db

class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        return {'id': playlist.id, 'name': playlist.name, 'user_id': playlist.user_id}

    def put(self, playlist_id):
        # Update a specific playlist by ID
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('audio_ids', type=int, action='append', required=False)
        args = parser.parse_args()

        playlist = Playlist.query.get_or_404(playlist_id)
        playlist.name = args['name']

        if args['audio_ids'] is not None:
            playlist.audio_records = AudioRecord.query.filter(AudioRecord.id.in_(args['audio_ids'])).all()

        db.session.commit()
        return {'message': 'Playlist updated successfully'}

    def delete(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        db.session.delete(playlist)
        db.session.commit()
        return '', 204

class PlaylistListResource(Resource):
    def get(self):
        playlists = Playlist.query.all()
        return [{'id': playlist.id, 'name': playlist.name} for playlist in playlists]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()

        playlist = Playlist(name=args['name'], user_id=args['user_id'])
        db.session.add(playlist)
        db.session.commit()
        return {'id': playlist.id}, 201
