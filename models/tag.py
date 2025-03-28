from infra import db
from datetime import datetime

class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Tag {self.name}>'
    

class ArticleTag(db.Model):
    __tablename__ = 'article_tag'
    
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

class ResourceTag(db.Model):
    __tablename__ = 'resource_tag'
    
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)