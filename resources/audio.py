from flask_restful import Resource, reqparse
from models import AudioRecord
from extensions import db

class AudioResource(Resource):
    def get(self, audio_id):
        audio = AudioRecord.query.get_or_404(audio_id)
        return {
            'id': audio.id,
            'title': audio.title,
            'genre': audio.genre.name,
            'user_id': audio.user_id,
            'release_date': audio.release_date.isoformat(),
            'audio_file_path': audio.audio_file_path
        }

    def put(self, audio_id):
        # Update a specific audio record by ID
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('artist', type=str, required=True)
        parser.add_argument('genre_id', type=int, required=True)
        parser.add_argument('release_date', type=str, required=True)
        parser.add_argument('audio_file_path', type=str, required=True)
        args = parser.parse_args()

        audio = AudioRecord.query.get_or_404(audio_id)
        audio.title = args['title']
        audio.artist = args['artist']
        audio.genre_id = args['genre_id']
        audio.release_date = args['release_date']
        audio.audio_file_path = args['audio_file_path']

        db.session.commit()
        return {'message': 'Audio record updated successfully'}

    def delete(self, audio_id):
        audio = AudioRecord.query.get_or_404(audio_id)
        db.session.delete(audio)
        db.session.commit()
        return '', 204

class AudioListResource(Resource):
    def get(self):
        audios = AudioRecord.query.all()
        return [{'id': audio.id, 'title': audio.title, 'genre': audio.genre.name} for audio in audios]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('genre_id', type=int, required=True)
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('release_date', type=str, required=True)
        parser.add_argument('audio_file_path', required=True)
        args = parser.parse_args()

        audio = AudioRecord(
            title=args['title'],
            genre_id=args['genre_id'],
            user_id=args['user_id'],
            release_date=args['release_date'],
            audio_file_path=args['audio_file_path']
        )
        db.session.add(audio)
        db.session.commit()
        return {'id': audio.id}, 201
