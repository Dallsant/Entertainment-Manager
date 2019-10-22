from app import db


class UserSeries(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    episodes = db.Column(db.Integer)
    left_at = db.Column(db.Integer, default=1)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    author = db.Column(db.String)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'),
                nullable=False)

    def __repr__(self):
        return f'Series: {self.id} - {self.name}'
