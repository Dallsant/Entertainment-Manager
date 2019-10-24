from endpoints.books.model import UserBook
from app import db
from app import logging

class UserBookRepository:
    def find(self):
        try:
            return UserBook.query.all()
        except Exception as error:
            raise error

    def findByName(self, name):
        try:
            book = UserBook.filter_by(name=name).first()
            if book:
                return book.__dict__
            else:
                return book
        except Exception as error:
            raise error    

    def findByUser(self, user_id):
        try:
            book = UserBook.filter_by(user_id=user_id)
            return book
        except Exception as error:
            raise error 

    def findById(self, id):
        try:
            book = UserBook.filter_by(id=id).first()
            if book:
                return book.__dict__
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