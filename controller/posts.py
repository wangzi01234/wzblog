from markdown import markdown
import os
import yaml  # 需要安装 pyyaml
from controller.minio import minio_client
from pymdownx.blocks import BlocksExtension


def parse_markdown(content):
    parts = content.split('---\r\n', 2)
    if len(parts) == 3:
        metadata = yaml.safe_load(parts[1])
        body = markdown(parts[2], extensions=['fenced_code', 'codehilite', 'tables'])
    else:
        metadata = {}
        body = markdown(parts[2], extensions=['fenced_code', 'codehilite', 'tables'])
    return metadata, body

def get_posts(category=None):
    posts = []
    prefix = f"{category}/" if category else ""
    objects = minio_client.list_objects(prefix)

    for obj in objects:
        if obj.object_name.endswith('.md'):
            content = minio_client.get_object(obj.object_name)
        else:
            continue
        if not content:
            continue
        try:
            metadata, content = parse_markdown(content)
            slug = os.path.splitext(os.path.basename(obj.object_name))[0]
            slug = slug.lower().replace(' ', '-')     
            metadata.setdefault('category', category if category else '未分类')
            metadata.setdefault('slug', slug)
            posts.append({**metadata, 'content': content})
        except Exception as e:
            app.logger.error(f"解析文件失败: {obj.object_name}, 错误: {str(e)}")
            continue
    
    # 安全排序：缺失日期的文章排最后
    return sorted(posts, key=lambda x: x.get('date'), reverse=True)