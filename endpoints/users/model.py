from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    # todos = db.relationship('Todo', backref='user', lazy='select')
    def __repr__(self):
        return f'Id: {self.id}, name: {self.name}, username: {self.username}, password:{self.password}, email:{self.email}'
