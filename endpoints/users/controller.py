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

user_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'content': fields.List(fields.Nested({'id': fields.Integer,
                                        'name': fields.String,
                                        'author': fields.String,
                                        }))
}

class ListUsersResource(Resource):
    def get(self):
        try:
            users = User.query.all()
            users = [marshal(user, user_list_fields) for user in users]
            return users

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class RegisterUser(Resource):
    def post(self):
        try:
            user = request.get_json()
            hashedPass = bcrypt.hashpw(
            user['password'].encode('utf-8'), bcrypt.gensalt())
            user['password'] = hashedPass.decode('utf-8')
            db.session.add(User(**user))
            db.session.commit()
            return marshal(user, user_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class UsersByIdResource(Resource):
    def get(self, id=None):
        user = User.query.filter_by(id=id).first()
        return marshal(user, user_list_fields)

    def delete(self, id=None):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return marshal(user, user_list_fields)



