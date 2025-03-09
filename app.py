### **3. 修改 app.py 的解析逻辑**
from flask import Flask, render_template, abort, request
from controller.posts import get_posts
from controller.plans import get_plans, get_stats, get_calendar_data
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
    print(123)
    return render_template('index.html', posts=get_posts())

@app.route('/post/<slug>')
def show_post(slug):
    posts = get_posts()
    post = next((p for p in posts if p['slug'] == slug), None)
    return render_template('post.html', post=post) if post else abort(404)

@app.route('/tech')
def tech():
    posts = get_posts(category='tech')
    return render_template('category.html', 
                         posts=posts,
                         category_name='技术杂谈',
                         category_desc='这里分享技术开发心得')
@app.route('/lang')
def lang():
    posts = get_posts(category='lang')
    return render_template('category.html', 
                         posts=posts,
                         category_name='语言学习',
                         category_desc='这里分享语言学习心得')

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
            print(123)
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404