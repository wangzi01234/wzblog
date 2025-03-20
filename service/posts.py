from markdown import markdown
import os
import yaml  # 需要安装 pyyaml
from service.minio import minio_client
from sqlalchemy import desc, or_
from datetime import datetime
from models.article import Article
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError  # 更精确的异常捕获

def parse_markdown(content):
    """解析带 YAML Front Matter 的 Markdown 文件"""
    parts = content.split('---\r\n', 2)
    if len(parts) == 3:
        metadata = yaml.safe_load(parts[1])
        body = markdown(parts[2], extensions=['fenced_code', 'codehilite', 'tables'])
    else:
        metadata = {}
        body = markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])
    return metadata, body

def get_content(category, slug):
    try:
        path = category + '/' + slug + '.md'
        content = minio_client.get_object(path)
        metadata, result = parse_markdown(content)
    except Exception as e:
        app.logger.error(f"解析文件失败: {slug+'.md'}, 错误: {str(e)}")
    return result

def get_info(category=None):
    """从数据库获取分类文章的优化方法"""
    try:
        # 初始化基础查询
        query = Article.query
        
        # 添加分类过滤条件
        if category is not None:
            query = query.filter(Article.category == category)
        
        # 构建排序规则（优先日期倒序，其次标题正序）
        query = query.order_by(
            desc(Article.date),
            Article.title.asc()
        )

        # 执行查询并转换数据结构
        posts = [
            {
                'title': art.title,
                'date': art.date,
                'excerpt': art.excerpt or '',
                'category': art.category if art.category else 'post',
                'slug' : art.path.split('/')[-1].split('.md')[0],
                # 'slug' : art.path.split('.md')[0].lower().replace(' ', '-'),
                'path' : art.path,
                'tags': art.tags or []
                # 如果需要其他字段可在此扩展
            }
            for art in query.all()
        ]

        # 双保险排序（处理数据库未正确排序的情况）
        return sorted(
            posts,
            key=lambda x: x['date'] or datetime.min,  # 确保datetime已导入
            reverse=True
        )

    except SQLAlchemyError as e:  # 捕获数据库操作异常
        app.logger.error(f"数据库查询失败: {str(e)}")
        return []
    except Exception as e:  # 兜底异常处理
        app.logger.error(f"系统异常: {str(e)}")
        return []


