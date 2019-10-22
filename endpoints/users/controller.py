from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import User, RevokedToken
from app import db
from app import api
import bcrypt
import json
from utilities import responseSchema
from endpoints.books.controller import book_list_fields
from endpoints.manga.controller import manga_list_fields
from endpoints.series.controller import series_list_fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import time

response = responseSchema.ResponseSchema()

user_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'books': fields.List(fields.Nested(book_list_fields)),
    'manga': fields.List(fields.Nested(manga_list_fields)),
    'series': fields.List(fields.Nested(series_list_fields))
}

register_parser = reqparse.RequestParser()
register_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
register_parser.add_argument(
    'email', help='Field email cannot be blank', required=True)
register_parser.add_argument(
    'username', help='Field username cannot be blank', required=True)
register_parser.add_argument(
    'password', help='Field password cannot be blank', required=True)


class ListUsersResource(Resource):
    def get(self):
        try:
            users = User.query.all()
            users = [marshal(user, user_list_fields) for user in users]
            return users

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class RegisterUserResource(Resource):
    def post(self):
        try:
            user = register_parser.parse_args()
            hashedPass = bcrypt.hashpw(
                user['password'].encode('utf-8'), bcrypt.gensalt())
            user['password'] = hashedPass.decode('utf-8')
            db.session.add(User(**user))
            db.session.commit()
            return marshal(user, user_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UsersByIdResource(Resource):
    def get(self, id=None):
        try:
            user = User.query.filter_by(id=id).first()
            return marshal(user, user_list_fields)
        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    def delete(self, id=None):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return marshal(user, user_list_fields)


login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'username', help='Field username cannot be blank', required=True)
login_parser.add_argument(
    'password', help='Field password cannot be blank', required=True)


class LoginResource(Resource):
    def post(self):
        try:
            credentials = login_parser.parse_args()
            user = User.query.filter_by(
                username=credentials['username']).first().__dict__
            if(user == None):
                return {"message": "User not registered"}, 404
            if bcrypt.checkpw(credentials['password'].encode('utf8'), user['password'].encode('utf8')) == False:
                return {"message": "Password does not match"}, 422
            auth_token = create_access_token(identity=user['id'])
            return {"access_token": auth_token, "message": f"logged in as {user.username}"}, 200

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class LogoutResource(Resource):
    def post(self):
        try:
            jti = get_raw_jwt()['jti']
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class currentUserResource(Resource):
    def get(self):
        try:
            current_user = get_jwt_identity()
            return current_user, 200
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class TokenRefreshResource(Resource):
    def post(self):
        try:
            return {'message': 'Token refresh'}
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
