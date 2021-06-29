import hashlib
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from telechat.extensions import db


class User(UserMixin, db.Model):
    """聊天室用户表模型"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    nickname = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    email_hash = db.Column(db.String(128))
    messages = db.relationship('Message', back_populates='author', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_email_hash()

    def set_password(self, password: str) -> None:
        """根据明文用户口令设置用户口令HASH

        :param password: 明文用户口令
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """将给定明文用户口令与数据库中的HASH校验比对验证

        :param password: 待验证的明文用户口令
        :return: True 表示口令匹配，False 表示口令不匹配
        """
        return check_password_hash(self.password_hash, password)

    def generate_email_hash(self) -> None:
        """为已有邮件信息但未生成邮箱HASH的用户生成邮箱HASH"""
        if self.email is not None and self.email_hash is None:
            self.email_hash = hashlib.md5(self.email.strip().lower().encode('utf-8')).hexdigest()

    @property
    def gravatar(self):
        """该用户的 Gravatar 头像 URL"""
        return f"https://www.gravatar.com/avatar/{ self.email_hash }?d=retro"


class Message(UserMixin, db.Model):
    """消息表模型"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship('User', back_populates='messages')
