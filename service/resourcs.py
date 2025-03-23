from models import Resource

def get_resources():
    # 从数据库中检索所有未删除的资源
    resources = Resource.query.filter_by(deleted_at=None).all()
    
    # 将检索到的资源转换为所需的格式
    formatted_resources = []
    for resource in resources:
        formatted_resource = {
            "name": resource.name or "未命名",
            "link": resource.link or "#",
            "source": resource.source or "",
            "author": resource.author or "",
            "tags": [tag.name for tag in resource.tags]  # 从关联表中获取标签名称
        }
        formatted_resources.append(formatted_resource)
    
    return formatted_resources
