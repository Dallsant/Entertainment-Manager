from endpoints.series.model import UserSeries
from app import db

class UserSeriesRepository:
    def find(self):
        try:
            return UserSeries.query.all()
        except Exception as error:
            raise error

    def findByName(self, name):
        try:
            series = UserSeries.filter_by(name=name).first()
            if series:
                return series.__dict__
            else:
                return series
        except Exception as error:
            raise error    

    def findByUser(self, user_id):
        try:
            series = UserSeries.filter_by(user_id=user_id)
            return series
        except Exception as error:
            raise error 

    def findById(self, id):
        try:
            series = UserSeries.filter_by(id=id).first()
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

    def delete(self, id):
        try:
            db.session.delete(UserSeries.query.get(id))
            db.session.commit()
        except Exception as error:
            raise error


