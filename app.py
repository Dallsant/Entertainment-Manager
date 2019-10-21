from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import datetime
app = Flask(__name__)
jwt = JWTManager(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

db = SQLAlchemy(app)
api = Api(app)
api.prefix = '/api'

app.config['JWT_SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=settings.JWT_EXPIRATION)

from endpoints.users.controller import UsersByIdResource, RegisterUserResource, ListUsersResource
from endpoints.series.controller import UserSeriesResource, UserSeriesByIdResource
from endpoints.books.controller import UserBookResource, UserBookByIdResource
from endpoints.manga.controller import UserMangaResource, UserMangaByIdResource


api.add_resource(RegisterUserResource, '/register')
api.add_resource(UsersByIdResource, '/users/<int:id>')
api.add_resource(ListUsersResource, '/users')

api.add_resource(UserSeriesResource, '/series')
api.add_resource(UserSeriesByIdResource, '/series/<int:id>')

api.add_resource(UserBookResource, '/books')
api.add_resource(UserBookByIdResource, '/books/<int:id>')

api.add_resource(UserMangaResource, 'manga/')
api.add_resource(UserMangaByIdResource, '/manga/<int:id>')


if __name__ == '__main__':
    app.run()
