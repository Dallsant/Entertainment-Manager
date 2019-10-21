from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserSeries
from app import db
from app import api
from utilities import responseSchema

response = responseSchema.ResponseSchema()


series_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'episodes_amount': fields.Integer,
    'left_at':fields.Integer,
    'finished':fields.Boolean
}

class UserSeriesResource(Resource):
    def post(self):
        try:
            series = request.get_json()
            db.session.add(UserSeries(**series))
            db.session.commit()
            return marshal(series, series_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def get(self):
        try:
            series = UserSeries.query.all()
            response.successMessage(series)
            return marshal(series, series_list_fields)
        
        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

class UserSeriesByIdResource(Resource):
    def get(self, id=None):
        try:
            series = UserSeries.query.filter_by(id=id).first()
            return marshal(series, series_list_fields)

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__

    def delete(self, id):
        try:
            series = UserSeries.query.get(id)
            db.session.delete(series)
            db.session.commit()
            return marshal(series, series_list_fields) 

        except Exception as error:
            response.errorResponse(str(error))
            return response.__dict__