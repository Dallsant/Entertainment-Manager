from app import db


class ContentType(db.Model):
    __tablename__ = 'contentType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    userContent = db.relationship('UserContent', backref='type', lazy='select')
    
    def __repr__(self):
        return 'Id: {}'.format(self.id)
