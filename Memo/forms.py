from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Memo


class MemoForm(FlaskForm):
    title = StringField(
        "タイトル：",
        validators=[
            DataRequired("タイトルは必須入力です"),
            Length(max=10, message="10文字以下で入力してください"),
        ],
    )
    content = TextAreaField("内容：")
    submit = SubmitField("返信")

    def validate_title(self, title):
        memo = Memo.query.filter_by(title=title.data).first()
        if memo:
            raise ValidationError(
                f"タイトル「{title.data}」は既に存在します。別のタイトルを入力してください。"
            )
