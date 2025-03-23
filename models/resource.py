from datetime import datetime
from infra import db

class Resource(db.Model):
    __tablename__ = 'resource'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255))
    category = db.Column(db.String(100))
    author = db.Column(db.String(100))
    detail = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    tags = db.relationship('Tag', secondary='resource_tag', backref=db.backref('resources', lazy=True))

    def __repr__(self):
        return f'<Resource {self.name}>'