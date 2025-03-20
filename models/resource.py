from datetime import datetime
from extensions import db

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

class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Tag {self.name}>'

# ResourceTag 模型通常不需要直接定义，因为它仅作为关联表存在。
# Flask-SQLAlchemy 会根据 resource 和 tag 模型以及它们之间的 relationship 自动处理。
# 但为了完整性，这里还是展示一下如何定义（尽管在实际应用中通常省略）：
class ResourceTag(db.Model):
    __tablename__ = 'resource_tag'
    
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # 注意：在实际应用中，通常不需要为关联表定义 __repr__ 方法，因为它主要用于表示资源或标签。
