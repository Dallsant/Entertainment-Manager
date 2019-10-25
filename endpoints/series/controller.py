from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import UserSeries
from app import db
from app import api
from utilities import responseSchema
import time
from .repository import UserSeriesRepository
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity)
import datetime
from app import logging
from services.error import err_handler
userSeriesRepository = UserSeriesRepository()

series_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'amount_of_episodes': fields.Integer,
    'left_at': fields.Integer,
    'finished': fields.Boolean,
    "user_id":fields.Integer
}

series_parser = reqparse.RequestParser()
series_parser.add_argument(
    'name', help='Field name cannot be blank', required=True)
series_parser.add_argument('amount_of_episodes', required=False)
series_parser.add_argument('left_at', required=False)
series_parser.add_argument('finished', required=False)


class UserSeriesResource(Resource):
    @jwt_required
    @err_handler
    def post(self):
        current_user = get_jwt_identity()
        series = series_parser.parse_args()
        existing_series = userSeriesRepository.findByName(series['name'], current_user['id'])
        print(marshal(existing_series, series_list_fields))
        if existing_series != None:
            return {'message': 'Resource already exists'}, 422
        series['user_id'] = current_user['id']
        userSeriesRepository.add(series)
        return marshal(series, series_list_fields)


    @jwt_required
    @err_handler
    def get(self):
        current_user = get_jwt_identity()
        print(current_user['id'])
        series = userSeriesRepository.findByUser(current_user['id'])
        return marshal(series, series_list_fields)


class UserSeriesByIdResource(Resource):
    @jwt_required
    @err_handler
    def get(self, id):
        current_user = get_jwt_identity()
        if current_user['id'] != id and not current_user['admin']:
            return {'message': 'Access Denied'}, 403
        series = userSeriesRepository.findById(id)
        return marshal(series, series_list_fields)

    @jwt_required
    @err_handler
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['id'] != id and not current_user['admin']:
            return {'message': 'Access Denied'}, 403
        userSeriesRepository.deleteById(id)
        return marshal(id, series_list_fields)

    # @err_handler
    # def put(self, id=None):
    #     current_user = get_jwt_identity()
    #     if current_user['id'] != id and not current_user['admin']:
    #         return {'message': 'Access Denied'}, 403
        
    #     updated_series = userSeriesRepository.update(id, series_parser.parse_args())
    #     series = UserSeries.query.get(id)

    #     db.session.commit()
    #     return todo