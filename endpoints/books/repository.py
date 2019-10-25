from endpoints.books.model import UserBook
from app import db
from app import logging

class UserBookRepository:
    def find(self):
        try:
            return UserBook.query.all()
        except Exception as error:
            raise error

    def findByName(self, name, user_id):
        try:
            book = UserBook.query.filter_by(name=name, user_id=user_id).first()
            if book:
                return book
            else:
                return book
        except Exception as error:
            raise error

    def findByUser(self, user_id):
        try:
            book = UserBook.query.filter_by(user_id=user_id)
            book = [serie for serie in book]
            return book
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            book = UserBook.query.filter_by(id=id).first()
            if book:
                return book
            else:
                return book
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserBook(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def deleteById(self, id):
        try:
            db.session.delete(UserBook.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error