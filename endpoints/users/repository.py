from endpoints.users.model import User, RevokedToken
from app import db


class UserRepository:
    def find(self):
        try:
            return User.query.all()
        except Exception as error:
            raise error

    def findByUsername(self, username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return user.__dict__
            else:
                return user

        except Exception as error:
            raise error

    def findById(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                return user.__dict__
            else:
                return user

        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(User(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def delete(self, id):
        try:
            db.session.delete(User.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error


class JWTRepository:
    def addRevokedToken(self, jti):
        try:
            db.session.add(RevokedToken(jti=jti))
            db.session.commit()
        except Exception as error:
            raise error
