from endpoints.books.model import UserBook
from app import db

class UserBookRepository:
    def find(self):
        try:
            return UserBook.query.all()
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            return UserBook.query.filter_by(id=id).first()
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserBook(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def delete(self, id):
        try:
            db.session.delete(UserBook.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error


