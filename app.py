from flask import Flask
from flask_restful import Api
from config import Config
from extensions import db
from flask_migrate import Migrate
from resources.user import UserResource, UserListResource
from resources.audio import AudioResource, AudioListResource
from resources.genre import GenreResource, GenreListResource
from resources.playlist import PlaylistResource, PlaylistListResource
from resources.listening_history import ListeningHistoryResource, ListeningHistoryListResource
from resources.role import RoleResource, RoleListResource

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(AudioListResource, '/audios')
api.add_resource(AudioResource, '/audios/<int:audio_id>')
api.add_resource(GenreListResource, '/genres')
api.add_resource(GenreResource, '/genres/<int:genre_id>')
api.add_resource(PlaylistListResource, '/playlists')
api.add_resource(PlaylistResource, '/playlists/<int:playlist_id>')
api.add_resource(ListeningHistoryListResource, '/listening_histories')
api.add_resource(ListeningHistoryResource, '/listening_histories/<int:history_id>')
api.add_resource(RoleListResource, '/roles')
api.add_resource(RoleResource, '/roles/<int:role_id>')

if __name__ == '__main__':
    app.run(debug=True)
