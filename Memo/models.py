from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy() # Flaskのappと未連携の状態で空インスタンスを生成

class Memo(db.Model):
	__tablename__ = 'memos'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(50), nullable=False)
	content = db.Column(db.Text) # 文字数無制限
