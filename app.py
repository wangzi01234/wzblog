### **3. 修改 app.py 的解析逻辑**
from flask import Flask, render_template, abort, request
from service.posts import get_info, get_content
from service.plans import get_plans, get_stats, get_calendar_data, get_target_date
from service.resourcs import get_resources
from service.category import get_category, get_categories, get_tags
from infra import db
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

@app.context_processor
def inject_global_data():
    # 获取需要全局使用的数据（如分类、标签等）
    return {
        'global_categories': get_categories(),
        'global_tags': get_tags()
    }

@app.route('/')
def index():
    posts=get_info()
    print(posts[0])
    return render_template('index.html', 
                           categories=get_categories(),
                           posts=get_info())

@app.route('/post/<category>/<slug>')
def show_post(category, slug):
    title, content = get_content(category, slug)
    return render_template('post.html', 
                           content=content, 
                           title=title 
                           if content else abort(404))

@app.route('/category/<category>')
def category(category):
    return render_template('category.html', 
                           posts=get_info(category=category), 
                           category=get_category(category) 
                           if category else abort(404))

@app.route('/tag/<tag>')
def tag(tag):
    return render_template('category.html', 
                           posts=get_info(tag=tag), 
                           category=get_category(category) 
                           if category else abort(404))

@app.route('/think')
def think():
    return render_template('think.html')

@app.route('/plan')
def plan():
    date_str = request.args.get('date') if 'date' in request.args else None
    # 初始化日期参数处理
    target_date = get_target_date(date_str)
    if not target_date:
        abort(400)
    return render_template('plan.html',
        year=target_date.year,
        month=target_date.month,
        current_date=target_date,
        calendar=get_calendar_data(target_date.year, target_date.month), # 获取日历数据
        today_plans=get_plans(target_date), # 获取计划数据
        stats = get_stats()
    )

@app.route('/filter')
def filter_posts():
    # 获取基础参数
    search_query = request.args.get('search', '')
    # 扩展参数示例（后续可在此添加其他参数）
    category = request.args.get('category', '')
    tags = request.args.getlist('tag')
    year = request.args.get('year', '')
    month = request.args.get('month', '')
    day = request.args.get('day', '')
    # 过滤文章
    posts=get_info(category=category, search=search_query)
    return render_template('index.html', posts=posts)

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

@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 404

if __name__ == '__main__':
    app.run(debug=True)