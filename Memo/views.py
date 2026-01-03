from flask import render_template, request, redirect, url_for, flash
from app import app # app.pyから取得
from models import db, Memo, User # models.pyから取得
from forms import MemoForm, LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required
from werkzeug.exceptions import NotFound # エラー画面用モジュールの追加

@app.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm() # ログインフォームクラスの読み込み
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.query.filter_by(username=username).first()
		# ユーザが存在し正しいパスワードであれば
		if user is not None and user.check_password(password):
			# ログイン状態に変換
			login_user(user)
			return redirect(url_for('index'))
		flash('認証不備です')
	return render_template('login_form.j2', form=form)

@app.route('/logout')
@login_required
def logout():
	# ログアウト状態に変換
	logout_user()
	flash('ログアウトしました')
	return redirect(url_for('login'))
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = SignUpForm() # 登録フォームクラスの読み込み
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User(username=username)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		flash('ユーザ登録しました')
		return redirect(url_for('login'))
	return render_template('register_form.j2', form=form)

@app.route('/memo/')
@login_required
def index():
	memos = Memo.query.all() # メモ全件取得
	return render_template('index.j2', memos=memos)

@app.route('/memo/create', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
