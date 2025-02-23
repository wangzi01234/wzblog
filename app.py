### **3. 修改 app.py 的解析逻辑**
from flask import Flask, render_template, abort
from controller.posts import get_posts
from controller.plans import get_plans, get_stats
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
from controller import posts, plans
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
    today = datetime.today().date()
    return render_template('plan.html', 
                         today_plans=get_plans(today),
                         stats=get_stats(),
                         current_date=today)

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/plans/<date>')
def daily_plans(date):
    target_date = datetime.strptime(date, '%Y-%m-%d').date()
    return render_template('plan.html',
                         today_plans=get_plans(target_date),
                         stats=get_stats(),
                         current_date=target_date)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404