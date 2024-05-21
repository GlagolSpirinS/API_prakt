from flask_restful import Resource, reqparse
from models import Genre
from extensions import db

class GenreResource(Resource):
    def get(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        return {'id': genre.id, 'name': genre.name}

    def delete(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return '', 204

class GenreListResource(Resource):
    def get(self):
        genres = Genre.query.all()
        return [{'id': genre.id, 'name': genre.name} for genre in genres]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        genre = Genre(name=args['name'])
        db.session.add(genre)
        db.session.commit()
        return {'id': genre.id}, 201
