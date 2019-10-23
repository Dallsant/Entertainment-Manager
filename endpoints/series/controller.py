from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserSeries
from app import db
from app import api
from utilities import responseSchema
import time
from flask_jwt_extended import ( jwt_required, jwt_refresh_token_required, get_jwt_identity)
# response = responseSchema.ResponseSchema()


series_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'amount_of_episodes': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean
}

series_parser = reqparse.RequestParser()
series_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
series_parser.add_argument('amount_of_episodes', required=False)
series_parser.add_argument('left_at', required=False)
series_parser.add_argument('finished', required=False)


class UserSeriesResource(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            series = series_parser.parse_args()
            series['user_id'] = current_user
            db.session.add(UserSeries(**series))
            db.session.commit()
            return marshal(series, series_list_fields)

        except Exception as error:
            print(error)
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    @jwt_required
    def get(self):
        try:
            series = UserSeries.query.all()
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500


class UserSeriesByIdResource(Resource):
    @jwt_required
    def get(self, id=None):
        try:
            series = UserSeries.query.filter_by(id=id).first()
            return marshal(series, series_list_fields)
        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500

    @jwt_required
    def delete(self, id):
        try:
            series = UserSeries.query.get(id)
            db.session.delete(series)
            db.session.commit()
            return marshal(series, series_list_fields)

        except Exception as error:
            return {'message': 'Something went wrong', 'timestamp': round(time.time())}, 500
