from endpoints.manga.model import UserManga
from app import db
from app import logging

class UserMangaRepository:
    def find(self):
        try:
            return UserManga.query.all()
        except Exception as error:
            raise error

    def findByName(self, name, user_id):
        try:
            manga = UserManga.query.filter_by(name=name, user_id=user_id)
            if manga:
                return manga.__dict__
            else:
                return manga
        except Exception as error:
            raise error

    def findByUser(self, user_id):
        try:
            manga = UserManga.query.filter_by(user_id=user_id)
            manga = [serie for serie in manga]
            return manga
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            if manga:
                return manga.__dict__
            else:
                return manga
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserManga(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def deleteById(self, id):
        try:
            db.session.delete(UserManga.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error