from app import db


class UserContent(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'),
                nullable=False)
    content_type_id = db.Column(db.Integer(), db.ForeignKey('contentType.id'),
                nullable=False)

    def __repr__(self):
        return 'Id: {}'.format(self.id)
