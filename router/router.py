# router/router.py
from flask import Blueprint, render_template, abort, request
from service.posts import get_info, get_content
from service.plans import get_plans, get_stats, get_calendar_data, get_target_date
from service.resources import get_resources
from service.category import get_category, get_categories, get_tags, get_tag
from datetime import datetime

bp = Blueprint('/', __name__)

@bp.context_processor
def inject_global_data():
    return {
        'global_categories': get_categories(),
        'global_tags': get_tags()
    }

@bp.route('/')
def index():
    """处理首页请求"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    posts_data = get_info(page=page, per_page=per_page)
    return render_template('posts.html', posts=posts_data['items'], pagination=posts_data['pagination'],
                           posts_title={'name': '最新文章', 'description':''}, title = 'WANGZI - 最新文章')

@bp.route('/category/<category>')
def category(category):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    posts_data = get_info(page=page, per_page=per_page, category=category)
    posts_title=get_category(category)
    return render_template('posts.html', posts=posts_data['items'], pagination=posts_data['pagination'],
                         posts_title=posts_title, title = "WANGZI - {}".format(posts_title['name'])) if category else abort(404)

@bp.route('/tag/<tag>')
def tag(tag):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    posts_data = get_info(page=page, per_page=per_page, tags=[tag])
    posts_title=get_tag(tag)
    return render_template('posts.html', posts=posts_data['items'], pagination=posts_data['pagination'],
                         posts_title=posts_title, title = "WANGZI - {}".format(posts_title['name'])) if tag else abort(404)

@bp.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search_query = request.args.get('search', '')
    posts_data = get_info(page=page, per_page=per_page, search=search_query)

    return render_template('posts.html', posts=posts_data['items'], pagination=posts_data['pagination'],
                           posts_title={'name': '搜索', 'description':''}, title = "WANGZI - 搜索")

@bp.route('/filter')
def filter():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    category = request.args.get('category', '')
    tags = request.args.get('tags', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    posts_data = get_info(page=page, per_page=per_page, tags=[t.strip() for t in tags.split(',') if t.strip()], category=category, start_date=start_date, end_date=end_date)

    return render_template('posts.html', posts=posts_data['items'], pagination=posts_data['pagination'],
                           posts_title={'name': '搜索', 'description':''}, title = "WANGZI - 搜索")

@bp.route('/post/<category>/<slug>')
def show_post(category, slug):
    title, content = get_content(category, slug)
    return render_template('post.html', 
                         content=content, 
                         title=title) if content else abort(404)

@bp.route('/think')
def think():
    return render_template('think.html')

@bp.route('/plan')
def plan():
    date_str = request.args.get('date') if 'date' in request.args else None
    target_date = get_target_date(date_str)
    if not target_date:
        abort(400)
    return render_template('plan.html',
        year=target_date.year,
        month=target_date.month,
        current_date=target_date,
        calendar=get_calendar_data(target_date.year, target_date.month),
        today_plans=get_plans(target_date),
        stats = get_stats()
    )

@bp.route('/book')
def book():
    return render_template('book.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/resource')
def resource():
    return render_template('resource.html', 
                        resources = get_resources(),
                        category_name='资源分享',
                        category_desc='各类资源分享')

@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400