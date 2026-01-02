from flask import render_template, request, redirect, url_for, flash
from app import app # app.pyから取得
from models import db, Memo # models.pyから取得
from forms import MemoForm
from werkzeug.exceptions import NotFound # エラー画面用モジュールの追加

@app.route('/memo/')
def index():
	memos = Memo.query.all() # メモ全件取得
	return render_template('index.j2', memos=memos)

@app.route('/memo/create', methods=['GET', 'POST'])
def create():
  form = MemoForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    memo = Memo(title=title, content=content)
    db.session.add(memo)
    db.session.commit()
    flash('登録しました')
    return redirect(url_for('index'))
  return render_template('create_form.j2', form=form)

@app.route('/memo/update/<int:memo_id>', methods=['GET', 'POST'])
def update(memo_id):
  target_data = Memo.query.get_or_404(memo_id) # 見つからない場合は404エラー
  form = MemoForm(obj=target_data)
  if request.method == 'POST' and form.validate():
    target_data.title = form.title.data
    target_data.content = form.content.data
    db.session.commit()
    flash('変更しました')
    return redirect(url_for('index'))
  return render_template('update_form.j2', form=form, edit_id = target_data.id) # 1件分をフォームに渡す

@app.route('/memo/delete/<int:memo_id>')
def delete(memo_id):
  memo = Memo.query.get_or_404(memo_id)
  db.session.delete(memo)
  db.session.commit()
  flash('変更しました')
  return redirect(url_for('index'))

@app.errorhandler(NotFound) # 404のNotFoundエラーが起きた際に実行
def show_404_page(error):
	msg = error.description # エラーメッセージを取得
	print(f'エラー内容：{msg}')
	return render_template('errors/404.j2', msg=msg), 404
