from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_moment import Moment

db = SQLAlchemy()               # 数据库 ORM
login_manager = LoginManager()  # 登录状态管理
csrf = CSRFProtect()            # CSRF 令牌管理
moment = Moment()               # 时间格式化管理
