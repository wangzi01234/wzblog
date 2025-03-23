from models import Category, Tag

def get_category(slug):
    # 从数据库中检索所有未删除的资源
    category = Category.query.filter_by(deleted_at=None).filter_by(slug=slug).first()
    if not category:
        return None
    # 将检索到的资源转换为所需的格式
    formatted_category = {
        "name": category.name or "",
        "description": category.description or "",
    }

    return formatted_category

def get_categories():
    # 从数据库中检索所有未删除的资源
    categories = Category.query.filter_by(deleted_at=None).all()
    if not categories:
        return []
    # 将检索到的资源转换为所需的格式
    formatted_categories = [
        {
            "name": category.name or "",
            "slug": category.slug or "",
            "description": category.description or "",
        }
        for category in categories
    ]

    return formatted_categories


def get_tags():
    # 从数据库中检索所有未删除的资源
    tags = Tag.query.filter_by(deleted_at=None).all()
    if not tags:
        return []
    # 将检索到的资源转换为所需的格式
    formatted_tags = [
        {
            "name": tag.name or "",
            "slug": tag.slug or "",
        }
        for tag in tags
    ]

    return formatted_tags