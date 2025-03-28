# app.py
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from infra import db
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # 应用工厂函数
    app = Flask(__name__)
    app.config['CONTENT_DIR'] = 'content'
    app.config.from_prefixed_env()
    
    # 初始化数据库
    db.init_app(app)
    
    # 配置日志
    configure_logger(app)
    
    # 注册路由蓝图
    register_blueprints(app)
    
    return app

def configure_logger(app):
    """配置日志记录器"""
    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # 文件日志处理器（自动轮转）
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=1024 * 1024 * 10,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 控制台日志处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    # 移除默认处理器，添加自定义处理器
    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    
    # 设置日志级别
    app.logger.setLevel(logging.DEBUG)
    
    # 禁止传播到根日志记录器
    app.logger.propagate = False

def register_blueprints(app):
    """注册所有蓝图"""
    from router.router import bp as router_bp
    app.register_blueprint(router_bp)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)