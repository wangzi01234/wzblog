from models import Plan

def get_plans(date):
    return Plan.query.filter_by(plan_date=date).all()

def get_stats():
    stats = {}
    categories = ['work', 'study', 'health', 'life']
    for cat in categories:
        total = Plan.query.filter_by(category=cat).count()
        completed = Plan.query.filter_by(category=cat, is_completed=True).count()
        stats[cat] = {'total': total, 'completed': completed}
    return stats