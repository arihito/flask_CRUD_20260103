from flask import render_template
from app import app
from werkzeug.exceptions import NotFound # エラー画面用モジュールの追加

@app.errorhandler(NotFound) # 404のNotFoundエラーが起きた際に実行
def show_404_page(error):
	msg = error.description # エラーメッセージを取得
	print(f'エラー内容：{msg}')
	return render_template('errors/404.j2', msg=msg), 404
