from datetime import datetime
from extensions import db

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(255))
    path = db.Column(db.String(255), nullable=False, unique=True)  # 路径唯一约束
    tags = db.Column(db.JSON)
    excerpt = db.Column(db.Text)
    body = db.Column(db.Text)

    def __repr__(self):
        return f'<Article {self.path}>'
