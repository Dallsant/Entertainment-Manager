from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserManga
from app import db
from app import api
from utilities import responseSchema

response = responseSchema.ResponseSchema()


manga_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'chapters_amount': fields.Integer,
    'left_at':fields.Integer,
    'finished':fields.Boolean,
    'author': fields.String
}

class UserMangaResource(Resource):
    def post(self):
        try:
            manga = request.get_json()
            db.session.add(UserManga(**manga))
            db.session.commit()
            return marshal(manga, manga_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            manga = UserManga.query.all()
            response.successMessage(manga)
            return marshal(manga, manga_list_fields)
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class UserMangaByIdResource(Resource):
    def get(self, id=None):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            return marshal(manga, manga_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            manga = UserManga.query.get(id)
            db.session.delete(manga)
            db.session.commit()
            return marshal(manga, manga_list_fields) 

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__