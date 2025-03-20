from models import Plan
from datetime import datetime, timedelta
import calendar as cal

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

def get_calendar_data(year, month):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, cal.monthrange(year, month)[1])
    # 生成日历数据
    weeks = []
    week = []
    
    # 填充上月日期
    prev_month_last_day = first_day - timedelta(days=1)
    prev_days = prev_month_last_day.weekday()  # 获取前个月最后一天的星期（0-6对应周一到周日）
    if prev_days != 6:
        for d in range(prev_days, -1, -1):
            day = prev_month_last_day - timedelta(days=d)
            week.append({
                'day': day.day,
                'month': day.month,
                'date': day.strftime('%Y-%m-%d')
            })
    
    current_day = first_day
    # print(current_day)
    while current_day <= last_day:
        if len(week) == 7:
            weeks.append(week)
            week = []
        week.append({
            'day': current_day.day,
            'month': current_day.month,
            'date': current_day.strftime('%Y-%m-%d')
        })
        current_day += timedelta(days=1)
    # print(week)
    # 填充下月日期
    next_month_first_day = last_day + timedelta(days=1)
    while len(week) < 7:
        week.append({
            'day': next_month_first_day.day,
            'month': next_month_first_day.month,
            'date': next_month_first_day.strftime('%Y-%m-%d')
        })
        next_month_first_day += timedelta(days=1)
    weeks.append(week)
    
    return weeks