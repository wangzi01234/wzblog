from datetime import datetime
from infra import db  # 确保 infra 模块已正确导出 SQLAlchemy 实例

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)  # 明确业务日期字段
    category = db.Column(db.String(255), index=True)  # 建议添加索引优化查询
    path = db.Column(db.String(255), nullable=False, unique=True)
    excerpt = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP(timezone=False),  # 明确非时区类型
                          comment='记录创建时间')
    deleted_at = db.Column(db.TIMESTAMP(timezone=False), 
                          nullable=True, 
                          comment='逻辑删除时间戳，NULL表示未删除')

    def soft_delete(self):
        """执行逻辑删除操作"""
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """恢复已删除的记录"""
        self.deleted_at = None

    def __repr__(self):
        return f'<Article {self.path}>'
