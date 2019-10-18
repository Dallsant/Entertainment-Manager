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

content_type_fields = {
    'count': fields.Integer,
    'content_types': fields.List(fields.Nested(content_type_fields)),
}

class ContentTypes(Resource):
    def post(self):
        try:
            content = request.get_json()
            db.session.add(ContentTypes(**content))
            db.session.commit()
            response.customResponse(False, "Content Type Added")
            return response.__dict__

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            content_type = ContentType.query.all()
            content_type = marshal({
                'count': len(content_type),
                'users': content_type
            }, content_type_fields)
            response.successMessage(content_type)
            return response.__dict__ 
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__


class ContentTypeById(Resource):
    def get(self, id=None):
        try:
            content_type = ContentType.query.filter_by(id=id).first()
            response.successMessage(content_type)
            return response.__dict__ 
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            content_type = ContentType.query.get(id)
            db.session.delete(content_type)
            db.session.commit()
            response.successMessage()
            return response.__dict__ 
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__