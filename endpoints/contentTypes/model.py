from app import db


class ContentType(db.Model):
    __tablename__ = 'Content Type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Id: {}, name: {}'.format(self.id, self.name)
