from app import db


class UserContent(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content_type_id = db.Column(db.Integer(100), nullable=False)
    user_id = db.Column(db.Integer(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        return f'{self.name}, {self.author}'
