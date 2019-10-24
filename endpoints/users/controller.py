from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal
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
import datetime
from .repository import UserRepository, JWTRepository
from app import logging

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
            print(4/0)
            current_user = get_jwt_identity()
            if not current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            users = userRepository.find()
            return marshal(users, user_list_fields)
        except Exception as error:
            logging.error(f'{error}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500


class RegisterUserResource(Resource):
    def post(self):
        try:
            credentials = register_parser.parse_args()
            user = userRepository.findByUsername(credentials['username'])
            if(user):
                return {'message': 'User Already Registered', 'timestamp': round(time.time())}, 500
            hashedPass = bcrypt.hashpw(
                credentials['password'].encode('utf-8'), bcrypt.gensalt())
            credentials['password'] = hashedPass.decode('utf-8')
            userRepository.add(credentials)
            return marshal(credentials, user_list_fields)

        except Exception as error:
            logging.error(f'{error}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500


class UsersByIdResource(Resource):
    @jwt_required
    def get(self, id=None):
        try:
            current_user = get_jwt_identity()
            if current_user['id'] != id and current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            user = userRepository.findById(id)
            return marshal(user, user_list_fields)
        except Exception as error:
            logging.error(f'{error}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['id'] != id and current_user['admin']:
            return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
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
            user = userRepository.findByUsername(credentials['username'])
            if not user:
                return {"message": "User not registered"}, 404
            if not bcrypt.checkpw(credentials['password'].encode('utf8'), user['password'].encode('utf8')):
                return {"message": "Password does not match"}, 422
            payload = {'id':user['id'], 'user':user['username'], 'admin':user['admin']}
            auth_token = create_access_token(identity=payload)
            return {"access_token": auth_token}, 200

        except Exception as error:
            logging.error(f'{error}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500


class LogoutResource(Resource):
    @jwt_required
    def get(self):
        try:
            jti = get_raw_jwt()['jti']
            jwtRepository.addRevokedToken(jti)
            return jti, 200
        except:
            logging.error(f'{error}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500
