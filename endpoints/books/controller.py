from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserBook
from app import db
from app import api
from utilities import responseSchema
import time
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity)
from .repository import UserBookRepository
import datetime
from app import logging

userBookRepository = UserBookRepository()

book_parser = reqparse.RequestParser()
book_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
book_parser.add_argument('chapters_amount', required=False)
book_parser.add_argument('left_at', required=False)
book_parser.add_argument('finished', required=False)
book_parser.add_argument('author', required=False)

book_list_fields = {
    'id': fields.Integer,
    'amount_of_pages': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean,
    'author': fields.String
}



class UserBookResource(Resource):
    @jwt_required
    def post(self):
       current_user = get_jwt_identity() 
        try:
            book = request.get_json()
            existing_book = userBookRepository.findByName(book['name'])
            if existing_book['name'] == book['name'] and existing_book['user_id'] == current_user['id']:
                return {'message': 'Resource already exists', 'time': datetime.datetime.now().isoformat()}, 422
            book['user_id'] = current_user['id']
            userBookRepository.add(book)
            return marshal(book, book_list_fields)

        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500

    @jwt_required
    def get(self):
       current_user = get_jwt_identity() 
        try:
            book = userBookRepository.findByUser(current_user['id'])
            return marshal(book, book_list_fields)
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500


class UserBookByIdResource(Resource):
    @jwt_required
    def get(self, id):
       current_user = get_jwt_identity() 
        try:
            if current_user['id'] != id and not current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            book = userBookRepository.findById(id)
            return marshal(book, book_list_fields)
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500

    @jwt_required
    def delete(self, id):
       current_user = get_jwt_identity() 
        try:
            if current_user['id'] != id and not current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            userBookRepository.deleteById(id)
            return id, 20
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500
