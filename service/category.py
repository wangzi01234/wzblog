from models.category import Category

def get_category(slug):
    # 从数据库中检索所有未删除的资源
    categories = Category.query.filter_by(deleted_at=None).filter_by(slug=slug).all()
    if len(categories) == 0:
        return None
    category = categories[0]
    # 将检索到的资源转换为所需的格式
    formatted_category = {
        "name": category.name or "",
        "description": category.description or "",
    }

    return formatted_category
