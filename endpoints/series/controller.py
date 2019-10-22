from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserSeries
from app import db
from app import api
from utilities import responseSchema
import time

response = responseSchema.ResponseSchema()


series_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'episodes_amount': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean
}

series_parser = reqparse.RequestParser()
series_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
series_parser.add_argument('episodes_amount', required=False)
series_parser.add_argument('left_at', required=False)
series_parser.add_argument('finished', required=False)


class UserSeriesResource(Resource):
    def post(self):
        try:
            series = series_parser.parse_args()
            db.session.add(UserSeries(**series))
            db.session.commit()
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    def get(self):
        try:
            series = UserSeries.query.all()
            response.successMessage(series)
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UserSeriesByIdResource(Resource):
    def get(self, id=None):
        try:
            series = UserSeries.query.filter_by(id=id).first()
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    def delete(self, id):
        try:
            series = UserSeries.query.get(id)
            db.session.delete(series)
            db.session.commit()
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
