from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager
from auth.views import auth_bp
from memo.views import memo_bp

app = Flask(__name__)

# 設定ファイルからConfigクラスを読み込み
app.config.from_object('config.Config')

# SQLAlchemyとFlaskAppの連携
db.init_app(app)
# Flask(App)とSQLAlchemy(DB)とマイグレーションの連携
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app) # Flaskアプリに紐付け
# アクセス制限ページからリダイレクト後のflashメッセージ
login_manager.login_message = '認証していません：ログインしてください'
login_manager.login_view = 'auth.login' # 不正アクセスはログインページへ
# Blueprintをアプリに紐付け
app.register_blueprint(auth_bp)
app.register_blueprint(memo_bp)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# CRUD+404(Views:routing→Template)の展開
from views import * # noqa: F403 E402

if __name__ == '__main__':
	app.run()
