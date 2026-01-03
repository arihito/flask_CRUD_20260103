from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy() # Flaskのappと未連携の状態で空インスタンスを生成

class Memo(db.Model):
	__tablename__ = 'memos'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(50), nullable=False)
	content = db.Column(db.Text) # 文字数無制限

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	# ハッシュ化したパスワードを上記のカラムに保持
	def set_password(self, password):
		self.password = generate_password_hash(password)
	# 保持したハッシュパスワードと渡された平文のパスワードと認証し真偽値を返す
	def check_password(self, password):
		return check_password_hash(self.password, password)
