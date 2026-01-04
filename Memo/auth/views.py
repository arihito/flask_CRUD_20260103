from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, User
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/', methods=['GET', 'POST'])
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
			return redirect(url_for('memo.index'))
		flash('認証不備です')
	return render_template('auth/login_form.j2', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
	# ログアウト状態に変換
	logout_user()
	flash('ログアウトしました')
	return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
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
		return redirect(url_for('auth.login'))
	return render_template('auth/register_form.j2', form=form)
