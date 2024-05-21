from flask_restful import Resource, reqparse
from models import Role
from extensions import db

class RoleResource(Resource):
    def get(self, role_id):
        role = Role.query.get_or_404(role_id)
        return {'id': role.id, 'name': role.name}

    def put(self, role_id):
        # Update a specific role by ID
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        role = Role.query.get_or_404(role_id)
        role.name = args['name']

        db.session.commit()
        return {'message': 'Role updated successfully'}

    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return '', 204

class RoleListResource(Resource):
    def get(self):
        roles = Role.query.all()
        return [{'id': role.id, 'name': role.name} for role in roles]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        role = Role(name=args['name'])
        db.session.add(role)
        db.session.commit()
        return {'id': role.id}, 201
