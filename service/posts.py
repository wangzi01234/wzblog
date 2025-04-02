import yaml
import json
from markdown import markdown
from infra import minio_client
from datetime import datetime
from models import Article, ArticleTag, Tag
from sqlalchemy import TypeDecorator, Text, desc, func, or_, and_
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from sqlalchemy.orm import joinedload

from datetime import datetime, date

class JSONDict(TypeDecorator):
    """自定义JSON字典类型处理器"""
    impl = Text
    cache_ok = True
    def process_result_value(self, value, dialect):
        try:
            return json.loads(value) if value else {}
        except (TypeError, json.JSONDecodeError):
            return {}
        

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
    path = '/articles/' + category + '/' + slug + '.md'
    try:
        content = minio_client.get_object(path)
        metadata, result = parse_markdown(content)
        title = metadata.get('title', '')
    except Exception as e:
        return None, None
    return title, result

# def get_info(category=None, tag=None, search=None):
#     """从数据库获取分类文章的优化方法"""
#     try:
#         query = Article.query
#         # 统一构建基础查询
#         posts_query = (
#             query
#             .outerjoin(ArticleTag, Article.id == ArticleTag.article_id)
#             .outerjoin(Tag, ArticleTag.tag_id == Tag.id)
#             .filter(Article.deleted_at.is_(None))
#         )
#         if tag:
#             # 创建子查询：获取包含该标签的文章ID
#             subquery = (
#                 ArticleTag.query
#                 .join(Tag, ArticleTag.tag_id == Tag.id)
#                 .filter(Tag.slug == tag)
#                 .with_entities(ArticleTag.article_id)
#                 .distinct()
#             )
#             # 主查询中过滤出这些文章
#             posts_query = posts_query.filter(Article.id.in_(subquery))
#         # 动态添加搜索条件
#         if search:
#             posts_query = posts_query.filter(
#                 or_(
#                     Article.title.ilike(f"%{search}%"),
#                     Tag.name.ilike(f"%{search}%")
#                 )
#             )

#         # 动态添加分类筛选条件
#         if category:
#             posts_query = posts_query.filter(Article.category == category)
            
#         # 继续构建完整查询
#         posts_query = posts_query.with_entities(
#             Article.id,
#             Article.title,
#             Article.date,
#             Article.excerpt,
#             Article.category,
#             Article.path,
#             func.JSON_OBJECTAGG(Tag.name, Tag.slug).cast(JSONDict).label('tags')
#         ).group_by(Article.id).order_by(desc(Article.date), Article.title.asc())

#         # 转换为结构化数据（避免N+1查询问题）
#         posts = [
#             {
#                 'id': art.id,
#                 'title': art.title,
#                 'date': art.date,
#                 'excerpt': art.excerpt or '',
#                 'category': art.category if art.category else 'post',
#                 'slug': art.path.split('/')[-1].split('.md')[0],
#                 'path': art.path,
#                 'tags': art.tags or None
#             }
#             for art in posts_query.all()
#         ]
        # # 双保险排序（处理数据库未正确排序的情况）
        # return sorted(
        #     posts,
        #     key=lambda x: x['date'] or datetime.min,  # 确保datetime已导入
        #     reverse=True
        # )

def get_info(page=1, per_page=15, category=None, tags=None, search=None, start_date=None, end_date=None):
    """优化后的分页查询方法"""
    # 日期参数处理
    default_start = date(2024, 1, 1)
    today = date.today()
    
    # 解析开始日期
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else default_start
    except (ValueError, TypeError):
        start_date = default_start
        
    # 解析结束日期
    try:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today
    except (ValueError, TypeError):
        end_date = today
        
    # 确保日期范围有效性
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    try:
        query = Article.query
        # 统一构建基础查询
        posts_query = (
            query
            .outerjoin(ArticleTag, Article.id == ArticleTag.article_id)
            .outerjoin(Tag, ArticleTag.tag_id == Tag.id)
            .filter(Article.deleted_at.is_(None))
            # 添加日期过滤条件
            .filter(and_(
                Article.date >= start_date,
                Article.date <= end_date
            ))
        )

        if tags:
            for tag in tags:
                # 创建子查询：获取包含该标签的文章ID
                subquery = (
                    ArticleTag.query
                    .join(Tag, ArticleTag.tag_id == Tag.id)
                    .filter(Tag.slug == tag)
                    .with_entities(ArticleTag.article_id)
                    .distinct()
                )
                # 主查询中过滤出这些文章
                posts_query = posts_query.filter(Article.id.in_(subquery))

        # 动态添加搜索条件
        if search:
            posts_query = posts_query.filter(
                or_(
                    Article.title.ilike(f"%{search}%"),
                    Tag.name.ilike(f"%{search}%")
                )
            )

        # 动态添加分类筛选条件
        if category:
            posts_query = posts_query.filter(Article.category == category)
            
        # 继续构建完整查询
        posts_query = posts_query.with_entities(
            Article.id,
            Article.title,
            Article.date,
            Article.excerpt,
            Article.category,
            Article.path,
            func.JSON_OBJECTAGG(Tag.name, Tag.slug).cast(JSONDict).label('tags')
        ).group_by(Article.id).order_by(desc(Article.date), Article.title.asc())

        # 执行分页查询
        pagination = posts_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            'items': [{
                'id': art.id,
                'title': art.title,
                'date': art.date,
                'excerpt': art.excerpt,
                'category': art.category,
                'path': art.path,
                'slug': art.path.split('/')[-1].split('.md')[0],
                'tags': art.tags
            } for art in pagination.items],
            'pagination': pagination
        }
    
    except SQLAlchemyError as e:
        error_info = {
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "sql_statement": str(posts_query),
            "params": posts_query.params
        }
        current_app.logger.error("数据库异常: %s", error_info)
        return []
    
    except Exception as e:
        current_app.logger.error("系统异常: %s", e)
        return []


