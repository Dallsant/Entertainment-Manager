from endpoints.series.model import MangaSeries
from app import db
from app import logging


class MangaSeriesRepository:
    def find(self):
        try:
            return MangaSeries.query.all()
        except Exception as error:
            raise error

    def findByName(self, name):
        try:
            series = MangaSeries.filter_by(name=name).first()
            if series:
                return series.__dict__
            else:
                return series
        except Exception as error:
            raise error

    def findByManga(self, Manga_id):
        try:
            series = MangaSeries.filter_by(Manga_id=Manga_id)
            return series
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            series = MangaSeries.filter_by(id=id).first()
            if series:
                return series.__dict__
            else:
                return series
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(MangaSeries(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def deleteById(self, id):
        try:
            db.session.delete(MangaSeries.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error
