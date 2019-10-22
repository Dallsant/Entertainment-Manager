from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserManga
from app import db
from app import api
from utilities import responseSchema

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
    def post(self):
        try:
            manga = request.get_json()
            db.session.add(UserManga(**manga))
            db.session.commit()
            return marshal(manga, manga_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    def get(self):
        try:
            manga = UserManga.query.all()
            response.successMessage(manga)
            return marshal(manga, manga_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UserMangaByIdResource(Resource):
    def get(self, id=None):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            return marshal(manga, manga_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    def delete(self, id):
        try:
            manga = UserManga.query.get(id)
            db.session.delete(manga)
            db.session.commit()
            return marshal(manga, manga_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
