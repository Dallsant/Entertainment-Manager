from endpoints.manga.model import UserManga
from app import db
from app import logging

class UserMangaRepository:
    def find(self, id):
        try:
            return UserManga.query.all()
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')


    def findByName(self, name):
        try:
            manga = UserManga.filter_by(name=name).first()
            if manga:
                return manga.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')
    

    def findByUser(self, user_id):
        try:
            manga = UserManga.filter_by(user_id=user_id)
            return manga
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')
 

    def findById(self, id):
        try:
            manga = UserManga.query.filter_by(id=id).first()
            if manga:
                return manga.__dict__
            else:
                return None
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')


    def add(self, data):
        try:
            db.session.add(UserManga(**data))
            db.session.commit()
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')


    def deleteById(self, id):
        try:
            db.session.delete(UserManga.query.get(id))
            db.session.commit()
        except Exception as error:
            logging.error(f'Manga Repository | {error} ')



