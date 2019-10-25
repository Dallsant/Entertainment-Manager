from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse, request
from app import logging
import datetime

def err_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            current_user = get_jwt_identity()
            logging.error(
                f'{request.method} | {request.url} | {e} | {request.remote_addr if current_user == None else current_user}')
            return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500
    return func_wrapper

# def handle_err(func):
#     def func_wrapper(self):
#         try:
#             return func(self)
#         except Exception as e:
#             current_user = get_jwt_identity()
#             logging.error(
#                 f'{request.method} | {request.url} | {e} | {request.remote_addr if current_user == None else current_user}')
#             return {'message': 'Something went wrong', 'time': datetime.datetime.now().isoformat()}, 500
#     return func_wrapper