from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_icon_path = db.Column(db.String(255))

    role = db.relationship('Role', back_populates='users')
    audio_records = db.relationship('AudioRecord', back_populates='user')
    playlists = db.relationship('Playlist', back_populates='user')
    listening_history = db.relationship('ListeningHistory', back_populates='user')

class AudioRecord(db.Model):
    __tablename__ = 'audio_records'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    release_date = db.Column(db.Date)
    audio_file_path = db.Column(db.String(255))

    genre = db.relationship('Genre', back_populates='audio_records')
    user = db.relationship('User', back_populates='audio_records')
    playlists = db.relationship('Playlist', secondary='playlist_audio', back_populates='audio_records')

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    audio_records = db.relationship('AudioRecord', back_populates='genre')

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='playlists')
    audio_records = db.relationship('AudioRecord', secondary='playlist_audio', back_populates='playlists')

class PlaylistAudio(db.Model):
    __tablename__ = 'playlist_audio'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    audio_id = db.Column(db.Integer, db.ForeignKey('audio_records.id'), primary_key=True)

class ListeningHistory(db.Model):
    __tablename__ = 'listening_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    audio_id = db.Column(db.Integer, db.ForeignKey('audio_records.id'))
    listened_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='listening_history')
    audio_record = db.relationship('AudioRecord')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    users = db.relationship('User', back_populates='role')
