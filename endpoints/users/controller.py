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
from .repository import UserRepository, JWTRepository

userRepository = UserRepository()
jwtRepository = JWTRepository()


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
    @jwt_required
    def get(self):
        try:
            users = userRepository.find()
            return marshal(users, user_list_fields)
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class RegisterUserResource(Resource):
    def post(self):
        try:
            credentials = register_parser.parse_args()
            user = userRepository.findByUsername(credentials['username'])
            if(bool(user)):
                return {'message': 'User Already Registered', 'timestamp': round(time.time())}, 500
            hashedPass = bcrypt.hashpw(
                credentials['password'].encode('utf-8'), bcrypt.gensalt())
            credentials['password'] = hashedPass.decode('utf-8')
            userRepository.add(credentials)
            return marshal(credentials, user_list_fields)

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UsersByIdResource(Resource):
    @jwt_required
    def get(self, id=None):
        try:
            user = userRepository.findById(id)
            return marshal(user, user_list_fields)
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    @jwt_required
    def delete(self, id=None):
        userRepository.delete(id)
        return id, 200


login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'username', help='Field username cannot be blank', required=True)
login_parser.add_argument(
    'password', help='Field password cannot be blank', required=True)


class LoginResource(Resource):
    def post(self):
        try:
            credentials = login_parser.parse_args()
            user = bool(userRepository.findByUsername(credentials['username']))
            if not user:
                return {"message": "User not registered"}, 404
            if not bcrypt.checkpw(credentials['password'].encode('utf8'), user['password'].encode('utf8')):
                return {"message": "Password does not match"}, 422

            auth_token = create_access_token(identity=user['id'])
            return {"access_token": auth_token}, 200

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class LogoutResource(Resource):
    @jwt_required
    def get(self):
        try:
            jti = get_raw_jwt()['jti']
            jwtRepository.addRevokedToken(jti)
            return jti, 200
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class currentUserResource(Resource):
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            return current_user, 200
        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
