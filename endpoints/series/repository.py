from endpoints.series.model import UserSeries
from app import db
from app import logging

class UserSeriesRepository:
    def find(self):
        try:
            return UserSeries.query.all()
        except Exception as error:
            raise error

    def findByName(self, name, user_id):
        try:
            series = UserSeries.query.filter_by(name=name, user_id=user_id)
            if series:
                return series.__dict__
            else:
                return series
        except Exception as error:
            raise error

    def findByUser(self, user_id):
        try:
            series = UserSeries.query.filter_by(user_id=user_id)
            series = [serie for serie in series]
            return series
        except Exception as error:
            raise error

    def findById(self, id):
        try:
            series = UserSeries.query.filter_by(id=id).first()
            if series:
                return series.__dict__
            else:
                return series
        except Exception as error:
            raise error

    def add(self, data):
        try:
            db.session.add(UserSeries(**data))
            db.session.commit()
        except Exception as error:
            raise error

    def deleteById(self, id):
        try:
            db.session.delete(UserSeries.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error

    # def update(self, id, updated_value):
    #     series = UserSeries.query.get(id)
    #     series = updated_value
    #     db.session.commit()