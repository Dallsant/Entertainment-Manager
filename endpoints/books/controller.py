from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserBook
from app import db
from app import api
from utilities import responseSchema
import time
from flask_jwt_extended import ( jwt_required, jwt_refresh_token_required, get_jwt_identity)

# response = responseSchema.ResponseSchema()

manga_parser = reqparse.RequestParser()
manga_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
manga_parser.add_argument('chapters_amount', required=False)
manga_parser.add_argument('left_at', required=False)
manga_parser.add_argument('finished', required=False)
manga_parser.add_argument('author', required=False)

book_list_fields = {
    'id': fields.Integer,
    'pages_amount': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean,
    'author': fields.String
}


class UserBookResource(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            book = request.get_json()
            book['user_id'] = current_user
            db.session.add(UserBook(**book))
            db.session.commit()
            return marshal(book, book_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
            
    @jwt_required
    def get(self):
        try:
            book = UserBook.query.all()
            return marshal(book, book_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UserBookByIdResource(Resource):
    @jwt_required
    def get(self, id=None):
        try:
            book = UserBook.query.filter_by(id=id).first()
            return marshal(book, book_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    @jwt_required   
    def delete(self, id):
        try:
            book = UserBook.query.get(id)
            db.session.delete(book)
            db.session.commit()
            return marshal(book, book_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
