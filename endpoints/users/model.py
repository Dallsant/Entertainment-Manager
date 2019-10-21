from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    series = db.relationship('UserSeries', backref='user', lazy='select')
    books = db.relationship('UserBook', backref='user', lazy='select')
    manga = db.relationship('UserManga', backref='user', lazy='select')

    def __repr__(self):
        return 'Id: {}'.format(self.id)
