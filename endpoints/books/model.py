from app import db


class UserBook(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pages_amount = db.Column(db.Integer)
    author = db.Column(db.String)
    left_at = db.Column(db.Integer, nullable=False, default=1)
    finished = db.Column(db.Boolean, nullable = False, default = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Id: {}'.format(self.id)
