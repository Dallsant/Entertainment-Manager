from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import User
from app import db
from app import api
import bcrypt


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    # 'todos': fields.List(fields.Nested({'id': fields.Integer,
    #                                     'name': fields.String,
    #                                     'description': fields.String})),
    'password': fields.String,
    'email':fields.String
}



user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}


class UsersResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return marshal(user, user_fields)
        else:
            args = request.args.to_dict()
            offset = args.get('offset', 0)
            args.pop('limit', None)
            args.pop('offset', None)

            user = User.query.filter_by(**args).order_by(User.id)

            if offset:
                user = user.offset(offset)

            user = user.all()

            return marshal({
                'count': len(user),
                'users': [marshal(u, user_fields) for u in user]
            }, user_list_fields)

    @marshal_with(user_fields)
    def post(self):
        try:
            user = request.get_json()
            # print(user)
            newUser = User(**user)
            # print("hello")
            print(newUser)
            db.session.add(newUser)
            db.session.commit()
        except Exception as e:
            print(e)


        return user

    @marshal_with(user_fields)
    def put(self, user_id=None):
        user = User.query.get(user_id)

        if 'name' in request.json:
            user.name = request.json['name']

        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, user_id=None):
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        return user
