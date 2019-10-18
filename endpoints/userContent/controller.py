from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserContent
from app import db
from app import api
from utilities import responseSchema

response = responseSchema.ResponseSchema()


content_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'author': fields.String
}

content_fields = {
    'count': fields.Integer,
    'content': fields.List(fields.Nested(content_fields)),
}

class UserContent(Resource):
    def post(self):
        try:
            content = request.get_json()
            db.session.add(UserContent(**content))
            db.session.commit()
            response.customResponse(False, "Content Added")
            return response.__dict__

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            content = UserContent.query.all()
            content = marshal({
                'count': len(content),
                'users': content
            }, content_fields)
            response.successMessage(content)
            return response.__dict__ 
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__


class ContentById(Resource):
    def get(self, id=None):
        try:
            content = UserContent.query.filter_by(id=id).first()
            response.successMessage(content)
            return response.__dict__ 
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            content = UserContent.query.get(id)
            db.session.delete(content)
            db.session.commit()
            response.successMessage()
            return response.__dict__ 
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__