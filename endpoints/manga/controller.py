from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserManga
from app import db
from app import api
from utilities import responseSchema
import time
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity)
import datetime
from .repository import UserMangaRepository
from app import logging

userMangaRepository = UserMangaRepository()

manga_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'amount_of_chapters': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean,
    'author': fields.String
}

manga_parser = reqparse.RequestParser()
manga_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
manga_parser.add_argument('amount_of_chapters', required=False)
manga_parser.add_argument('left_at', required=False)
manga_parser.add_argument('finished', required=False)
manga_parser.add_argument('author', required=False)


class UserMangaResource(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()        
        try:
            manga = request.get_json()
            existing_manga = userMangaRepository.findByName(manga['name'])
            if existing_manga['name'] == manga['name'] and existing_manga['user_id'] == current_user['id']:
                return {'message': 'Resource already exists', 'time': datetime.datetime.now().isoformat()}, 422
            manga['user_id'] = current_user['id']
            userMangaRepository.add(manga)
            return marshal(manga, manga_list_fields)

        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()        
        try:
            manga = userMangaRepository.findByUser(current_user['id'])
            return marshal(manga, manga_list_fields)
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500


class UserMangaByIdResource(Resource):
    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity()        
        try:
            if current_user['id'] != id and not current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            manga = userMangaRepository.findById(id)
            return marshal(manga, manga_list_fields)
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()        
        try:
            if current_user['id'] != id and not current_user['admin']:
                return {'message': 'Access Denied', 'time': datetime.datetime.now().isoformat()}, 403
            userMangaRepository.deleteById(id)
            return id, 200
        except Exception as error:
            logging.error(f'{request.method} | {request.url} | {error} | {current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500
