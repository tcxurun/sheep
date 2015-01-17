#encoding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(Form):
	username = StringField('用户名',validators=[Required(),Length(1,20)])
	password = PasswordField('密码',validators=[Required()])
	remember_me = BooleanField('记住密码')
	submit = SubmitField('登陆')

class ChangePasswordForm(Form):
	old_password = PasswordField('旧密码',validators=[Required()])
	password = PasswordField('新密码',validators=[Required(),EqualTo('password2',message='两次输入密码必须一致')])
	password2 = PasswordField('确认新密码',validators=[Required()])
	submit = SubmitField('更新密码')

class PasswordResetRequestForm(Form):
	email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
	submit = SubmitField('重置密码')

class PasswordResetForm(Form):
	email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
	password = PasswordField('新密码',validators=[Required(),EqualTo('password2',message='两次输入密码必须一致')])
	password2 = PasswordField('确认新密码',validators=[Required()]) 
	submit = SubmitField('重置密码')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('未知邮件地址。')

class ChangeEmailForm(Form):
	email = StringField('新邮箱',validators=[Required(),Length(1,64),Email()])
	password = PasswordField('密码',validators=[Required()])
	submit = SubmitField('更改邮箱地址')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('该邮件地址已存在')