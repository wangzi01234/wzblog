from datetime import datetime
from infra import db

class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.Enum('work', 'study', 'health', 'life'))
    plan_date = db.Column(db.Date)
    is_completed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Plan {self.title}>'