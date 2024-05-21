from flask_restful import Resource, reqparse
from models import ListeningHistory, Genre
from extensions import db

class ListeningHistoryResource(Resource):
    def get(self, history_id):
        history = ListeningHistory.query.get_or_404(history_id)
        return {
            'id': history.id,
            'user_id': history.user_id,
            'audio_id': history.audio_id,
            'listened_at': history.listened_at.isoformat()
        }

    def put(self, genre_id):
        # Update a specific genre by ID
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        genre = Genre.query.get_or_404(genre_id)
        genre.name = args['name']

        db.session.commit()
        return {'message': 'Genre updated successfully'}

    def put(self, history_id):
        # Update a specific listening history record by ID
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('audio_record_id', type=int, required=True)
        args = parser.parse_args()

        history = ListeningHistory.query.get_or_404(history_id)
        history.user_id = args['user_id']
        history.audio_record_id = args['audio_record_id']

        db.session.commit()
        return {'message': 'Listening history updated successfully'}

    def delete(self, history_id):
        history = ListeningHistory.query.get_or_404(history_id)
        db.session.delete(history)
        db.session.commit()
        return '', 204

class ListeningHistoryListResource(Resource):
    def get(self):
        history_list = ListeningHistory.query.all()
        return [{
            'id': history.id,
            'user_id': history.user_id,
            'audio_id': history.audio_id,
            'listened_at': history.listened_at.isoformat()
        } for history in history_list]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('audio_id', type=int, required=True)
        args = parser.parse_args()

        history = ListeningHistory(user_id=args['user_id'], audio_id=args['audio_id'])
        db.session.add(history)
        db.session.commit()
        return {'id': history.id}, 201
