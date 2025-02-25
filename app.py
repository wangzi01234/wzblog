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
    # 获取参数
    year = request.args.get('year', type=int, default=datetime.now().year)
    month = request.args.get('month', type=int, default=datetime.now().month)
    date_str = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))
    
    # 处理月份溢出
    if month > 12:
        year += 1
        month = 1
    elif month < 1:
        year -= 1
        month = 12
    
    try:
        current_date = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        current_date = datetime.now()
    
    # 生成日历数据
    calendar_data = get_calendar_data(year, month)
    
    # 获取当日计划
    today_plans = get_plans(current_date)
    
    # 渲染模板
    return render_template('plan.html',
                         year=year,
                         month=month,
                         current_date=current_date,
                         calendar=calendar_data,
                         today_plans=today_plans)

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/plan/<date>')
def daily_plans(date):
    target_date = datetime.strptime(date, '%Y-%m-%d').date()
    calendar_data = get_calendar_data(target_date.year, target_date.month)
    return render_template('plan.html',
                         today_plans=get_plans(target_date),
                         stats=get_stats(),
                         current_date=target_date,
                         calendar=calendar_data,
                         year=target_date.year,
                         month=target_date.month,
                         day=target_date.day
                         )
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404