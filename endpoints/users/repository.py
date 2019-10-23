from endpoints.users.model import User, RevokedToken

class UserRepository:

    def findByUsername(self, username):
        return User.query.filter_by(username=username).first()

    def findById(self, id):
        return User.query.filter_by(id=id).first()

    def add(self, data):
        db.session.add(User(**data))
        db.session.commit()

    def delete(self, id):
        db.session.delete(User.query.get(id))
        db.session.commit()
        
class JWTRepository:
    def addRevokedToken(self, jti):
        db.session.add(RevokedToken(jti=jti))
        db.session.commit()