import yaml
import json
from markdown import markdown
from infra import minio_client
from datetime import datetime
from models import Article, ArticleTag, Tag
from sqlalchemy import desc, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import TypeDecorator, Text

class JSONDict(TypeDecorator):
    """自定义JSON字典类型处理器"""
    impl = Text
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

def get_info(category=None, tag=None, search=None):
    """从数据库获取分类文章的优化方法"""
    try:
        query = Article.query
        # 统一构建基础查询
        posts_query = (
            query
            .outerjoin(ArticleTag, Article.id == ArticleTag.article_id)
            .outerjoin(Tag, ArticleTag.tag_id == Tag.id)
            .filter(Article.deleted_at.is_(None))
        )
        if tag:
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
        print(posts_query)
        # 转换为结构化数据（避免N+1查询问题）
        posts = [
            {
                'id': art.id,
                'title': art.title,
                'date': art.date,
                'excerpt': art.excerpt or '',
                'category': art.category if art.category else 'post',
                'slug': art.path.split('/')[-1].split('.md')[0],
                'path': art.path,
                'tags': art.tags or None
            }
            for art in posts_query.all()
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


