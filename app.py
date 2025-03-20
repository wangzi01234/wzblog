### **3. 修改 app.py 的解析逻辑**
from flask import Flask, render_template, abort, request
from service.posts import get_info, get_content
from service.plans import get_plans, get_stats, get_calendar_data
from service.resourcs import get_resources
from service.category import get_category
from extensions import db
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['CONTENT_DIR'] = 'csontent'
    app.config.from_prefixed_env()
    # app.config.from_pyfile('config.py')
    db.init_app(app)
    return app

app = create_app()

# ... 其他路由保持不变 ...
@app.route('/')
def index():
    return render_template('index.html', posts=get_info())

@app.route('/post/<category>/<slug>')
def show_post(category, slug):
    content = get_content(category, slug)
    return render_template('post.html', content=content, title=slug) if content else abort(404)

@app.route('/category/<category>')
def category(category):
    posts=get_info(category)
    category=get_category(category)
    if category is None:
        print("122222")
        abort(404)
    return render_template('category.html', 
                         posts=posts,
                         category=category)

@app.route('/think')
def think():
    return render_template('think.html')

@app.route('/plan')
def plan():
    # 初始化日期处理
    current_date = datetime.now()    
    try:
        # 优先级1：处理date查询参数
        if 'date' in request.args:
            date_str = request.args.get('date')
            current_date = datetime.strptime(date_str, '%Y-%m-%d')
            # 当存在date参数时，强制覆盖year/month参数
            year = current_date.year
            month = current_date.month
        else:
            # 优先级2：处理独立的year/month参数
            year = request.args.get('year', type=int, default=current_date.year)
            month = request.args.get('month', type=int, default=current_date.month)           
            # 处理月份溢出逻辑
            if month > 12:
                year += 1
                month = 1
            elif month < 1:
                year -= 1
                month = 12
            # 生成当前月份第一天作为参考日期
            current_date = datetime(year, month, 1)
    except ValueError as e:
        abort(400, description=f"Invalid date format: {str(e)}")
    # 获取准确的目标日期（处理可能存在的day参数）
    try:
        day = request.args.get('day', type=int, default=current_date.day)
        target_date = datetime(year, month, day).date()
    except ValueError:
        target_date = current_date.date()
    # 生成日历数据
    calendar_data = get_calendar_data(year, month)
    # 获取计划数据
    today_plans = get_plans(target_date)
    # 统一模板渲染
    return render_template('plan.html',
        year=year,
        month=month,
        current_date=target_date,
        calendar=calendar_data,
        today_plans=today_plans,
        stats=get_stats(),
    )

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resource')
def resource():
    return render_template('resource.html', 
                        resources = get_resources(),
                        category_name='资源分享',
                        category_desc='各类资源分享')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)