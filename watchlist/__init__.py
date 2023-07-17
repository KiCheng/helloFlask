import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# sys.platform 可以获取sys的操作系统
app = Flask(__name__)
# 数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # 等同于 app.secret_key = 'dev'

# Flask 提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 初始化扩展，传入程序实例 app
# 关系型数据库管理系统（RDBMS）的 SQLite，它基于文件，不需要单独启动数据库服务器
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):  # 接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 如果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示一个错误提示
login_manager.login_view = 'login'


# 对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # {'user':user},这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用


from watchlist import views, errors, commands