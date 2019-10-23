from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserManga
from app import db
from app import api
from utilities import responseSchema
import time 
from flask_jwt_extended import ( jwt_required, jwt_refresh_token_required, get_jwt_identity)
# response = responseSchema.ResponseSchema()


manga_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'chapters_amount': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean,
    'author': fields.String
}

manga_parser = reqparse.RequestParser()
manga_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
manga_parser.add_argument('chapters_amount', required=False)
manga_parser.add_argument('left_at', required=False)
manga_parser.add_argument('finished', required=False)
manga_parser.add_argument('author', required=False)


class UserMangaResource(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            manga = request.get_json()
            manga['user_id'] = current_user
            db.session.add(UserManga(**manga))
            db.session.commit()
            return marshal(manga, manga_list_fields)

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    @jwt_required
    def get(self):
        try:
            manga = UserManga.query.all()
            return marshal(manga, manga_list_fields)

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UserMangaByIdResource(Resource):
    @jwt_required
    def get(self, id=None):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            return marshal(manga, manga_list_fields)

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
   
    @jwt_required
    def delete(self, id):
        try:
            manga = UserManga.query.get(id)
            db.session.delete(manga)
            db.session.commit()
            return marshal(manga, manga_list_fields)

        except:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
