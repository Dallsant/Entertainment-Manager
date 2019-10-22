from app import db


class UserManga(db.Model):
    __tablename__ = 'manga'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapters_amount = db.Column(db.Integer)
    left_at = db.Column(db.Integer, nullable=False, default=1)
    finished = db.Column(db.Boolean, nullable = False, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                nullable=False)

    def __repr__(self):
        return f'Manga: {self.id} - {self.name}'
