from endpoints.series.model import UserSeries
from app import db

class UserSeriesRepository:
    def find(self):
        try:
            return UserSeries.query.all()
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            return UserSeries.query.filter_by(id=id).first()
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserSeries(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def delete(self, id):
        try:
            db.session.delete(UserSeries.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error


