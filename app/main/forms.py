#encoding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp,InputRequired
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import User

class EditProfileForm(Form):
    about_me = TextAreaField('关于我', validators=[Required()])
    submit = SubmitField('提交')

class PostForm(Form):
	title = StringField('标题',validators=[Required()])
	body = TextAreaField("正文",validators=[Required()])
	submit = SubmitField('提交')

class CommentForm(Form):
	nickname = StringField('昵称',validators=[Required()])
	body = StringField('内容', validators=[Required()])
	submit = SubmitField('提交')