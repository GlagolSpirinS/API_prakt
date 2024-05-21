from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from models import User
from extensions import db

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name,
            'avatar_icon_path': user.avatar_icon_path
        }


    def put(self, user_id):
        # Update a specific user by ID
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('role_id', type=int, required=True)
        parser.add_argument('avatar_icon_path', type=str, required=False)
        args = parser.parse_args()

        user = User.query.get_or_404(user_id)
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        user.role_id = args['role_id']
        user.avatar_icon_path = args.get('avatar_icon_path')

        db.session.commit()
        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id,
                 'username': user.username,
                 'email': user.email,
                 'avatar_icon_path': user.avatar_icon_path
        }
                for user in users]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role_id', type=int, required=True)
        parser.add_argument('avatar_icon_path')
        args = parser.parse_args()

        hashed_password = generate_password_hash(
            args['password'], method='pbkdf2:sha256'
        )

        user = User(
            username=args['username'],
            email=args['email'],
            password=hashed_password,  # Store the hashed password
            role_id=args['role_id'],
            avatar_icon_path=args.get('avatar_icon_path')
        )
        db.session.add(user)
        db.session.commit()
        return {'id': user.id}, 201
