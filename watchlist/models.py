from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class User(db.Model, UserMixin):  # 表名自动小写"user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    hash_password = db.Column(db.String(128))

    # 生成散列密码
    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.hash_password, password)  # 返回布尔值


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))