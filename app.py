### **3. 修改 app.py 的解析逻辑**
from flask import Flask, render_template, abort
from markdown import markdown
import os
import yaml  # 需要安装 pyyaml

app = Flask(__name__)
app.config['CONTENT_DIR'] = 'content'

def parse_markdown(content):
    """解析带 YAML Front Matter 的 Markdown 文件"""
    parts = content.split('---\n', 2)
    if len(parts) == 3:
        metadata = yaml.safe_load(parts[1])
        body = markdown(parts[2], extensions=['fenced_code', 'codehilite'])
    else:
        metadata = {}
        body = markdown(content, extensions=['fenced_code', 'codehilite'])
    return metadata, body

def get_posts(category=None):
    posts = []
    base_dir = app.config['CONTENT_DIR']
    
    target_dir = os.path.join(base_dir, category) if category else base_dir
    
    for root, _, files in os.walk(target_dir):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(root, filename)
            # print(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    # 解析元数据和内容
                    metadata, content = parse_markdown(f.read())
                    # print(metadata)
                    # print(type(metadata))
                    # 自动获取分类
                    rel_path = os.path.relpath(root, base_dir)
                    metadata.setdefault('category', rel_path if rel_path != '.' else '未分类') 
                    metadata.setdefault('slug', os.path.splitext(filename)[0])        
                    posts.append({**metadata, 'content': content})
                
            except Exception as e:
                app.logger.error(f"解析文件失败: {filepath}, 错误: {str(e)}")
                continue
    
    # 安全排序：缺失日期的文章排最后
    return sorted(posts, key=lambda x: x.get('date'), reverse=True)

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
    return render_template('plan.html')

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404