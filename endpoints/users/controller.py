from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import User
from app import db
from app import api
import bcrypt
import json
from utilities import responseSchema
# from sqlalchemy.orm import validates

response = responseSchema.ResponseSchema()


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}

class RegisterUser(Resource):
    def post(self):
        try:
            user = request.get_json()
            hashedPass = bcrypt.hashpw(
                user['password'].encode('utf-8'), bcrypt.gensalt())
            user['password'] = hashedPass.decode('utf-8')
            db.session.add(User(**user))
            db.session.commit()
            response.customResponse(False, "User Registered")
            return response.__dict__

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            user = User.query.all()
            user = marshal({
                'count': len(user),
                'users': user
            }, user_list_fields)
            response.successMessage(user)
            return response.__dict__ 
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class UsersResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return marshal(user, user_fields)

    def put(self, user_id=None):
        user = User.query.get(user_id)

        if 'name' in request.json:
            user.name = request.json['name']

        db.session.commit()
        return user

    def delete(self, user_id=None):
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        return user



