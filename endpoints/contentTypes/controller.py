from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import ContentType
from app import db
from app import api
from utilities import responseSchema

response = responseSchema.ResponseSchema()


content_type_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

content_type_list_fields = {
    'id': fields.Integer,
    'name': fields.String
    }

class ContentTypes(Resource):
    def post(self):
        try:
            content_type = request.get_json()
            db.session.add(ContentType(**content_type))
            db.session.commit()
            response.customResponse(False, "Content Type Added")
            return marshal(content_type, content_type_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            content_type = ContentType.query.all()
            content_type = marshal(content_type, content_type_list_fields)
            return content_type
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__


class ContentTypeById(Resource):
    def get(self, id=None):
        try:
            content_type = ContentType.query.filter_by(id=id).first()
            response.successMessage(content_type)
            return marshal(content_type, content_type_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            content_type = ContentType.query.get(id)
            db.session.delete(content_type)
            db.session.commit()
            return marshal(content_type, content_type_fields)
            
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__