from flask import Flask
from flask_migrate import Migrate
from models import db
app = Flask(__name__)

# 設定ファイルからConfigクラスを読み込み
app.config.from_object('config.Config')

# SQLAlchemyとFlaskAppの連携
db.init_app(app)
# Flask(App)とSQLAlchemy(DB)とマイグレーションの連携
migrate = Migrate(app, db)

# CRUD+404(Views:routing→Template)の展開
from views import * # noqa: F403 E402

if __name__ == '__main__':
	app.run()
