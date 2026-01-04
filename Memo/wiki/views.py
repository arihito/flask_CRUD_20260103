from flask import render_template, Blueprint
from wikipediaapi import Wikipedia
from forms import WikiForm
from flask_login import login_required

wiki_bp = Blueprint('wiki', __name__, url_prefix='/wiki')
wiki_ja = Wikipedia('ja') # 日本語Wikiのインスタンスを取得

@wiki_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	form = WikiForm()
	if form.validate_on_submit():
		keyword = form.keyword.data
		page = wiki_ja.page(keyword) # Wiki内検索
		if page.exists(): # 検索ページがあれば
			# 記事の要約文の最初の200文字文と、そのページのURLを絶対パスで取得
			return render_template('wiki/wiki_search_result.j2', \
			keyword=keyword, summary=page.summary[:200], url=page.fullurl)
		else:
			return render_template('wiki/wiki_search_result.j2', error='指定されたキーワードの結果は見つかりませんでした。')
	return render_template('wiki/wiki_search.j2', form=form) 
