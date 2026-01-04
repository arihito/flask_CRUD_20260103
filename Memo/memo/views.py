from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Memo
from forms import MemoForm
from flask_login import login_required, current_user

memo_bp = Blueprint('memo', __name__, url_prefix='/memo')

@memo_bp.route('/')
@login_required
def index():
	memos = Memo.query.filter_by(user_id=current_user.id).all() # メモ全件取得
	return render_template('memo/index.j2', memos=memos)

@memo_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = MemoForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    memo = Memo(title=title, content=content, user_id=current_user.id)
    db.session.add(memo)
    db.session.commit()
    flash('登録しました')
    return redirect(url_for('memo.index'))
  return render_template('memo/create_form.j2', form=form)

@memo_bp.route('/update/<int:memo_id>', methods=['GET', 'POST'])
@login_required
def update(memo_id):
  target_data = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404() # 見つからない場合は404エラー
  form = MemoForm(obj=target_data)
  if request.method == 'POST' and form.validate():
    target_data.title = form.title.data
    target_data.content = form.content.data
    db.session.commit()
    flash('変更しました')
    return redirect(url_for('memo.index'))
  return render_template('memo/update_form.j2', form=form, edit_id=target_data.id) # 1件分をフォームに渡す

@memo_bp.route('/delete/<int:memo_id>')
@login_required
def delete(memo_id):
  memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
  db.session.delete(memo)
  db.session.commit()
  flash('変更しました')
  return redirect(url_for('memo.index'))

@memo_bp.route('create_from_search', methods=['POSt'])
@login_required
def create_from_search():
	title = request.form['title']
	content = request.form['content']
	new_memo = Memo(title=title, content=content, user_id=current_user.id)
	db.session.add(new_memo)
	db.session.commit()
	flash('Wikiからデータ登録しました')
	return redirect(url_for('memo.index'))

@memo_bp.route('/show/<int:memo_id>')
@login_required
def show(memo_id):
  target_data = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404() # 見つからない場合は404エラー
  return render_template('memo/show.j2', show=target_data)
