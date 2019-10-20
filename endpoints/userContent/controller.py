from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserContent
from app import db
from app import api
from utilities import responseSchema

response = responseSchema.ResponseSchema()


content_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'author': fields.String
}

class ContentResource(Resource):
    def post(self):
        try:
            content = request.get_json()
            db.session.add(UserContent(**content))
            db.session.commit()
            return marshal(content, content_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            content = UserContent.query.all()
            response.successMessage(content)
            return marshal(content, content_list_fields)
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class ContentById(Resource):
    def get(self, id=None):
        try:
            content = UserContent.query.filter_by(id=id).first()
            return marshal(content, content_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            content = UserContent.query.get(id)
            db.session.delete(content)
            db.session.commit()
            return marshal(content, content_list_fields) 

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__