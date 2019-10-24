from endpoints.manga.model import UserManga
from app import db

class UserMangaRepository:
    def find(self, id):
        try:
            return UserManga.query.all()
        except Exception as error:
            raise error

    def findByName(self, name):
        try:
            manga = UserManga.filter_by(name=name).first()
            if manga:
                return manga.__dict__
            else:
                return None
        except Exception as error:
            raise error    

    def findByUser(self, user_id):
        try:
            manga = UserManga.filter_by(user_id=user_id)
            return manga
        except Exception as error:
            raise error 

    def findById(self, id):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            if manga:
                return manga.__dict__
            else:
                return None
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserManga(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def delete(self, id):
        try:
            db.session.delete(UserManga.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error


