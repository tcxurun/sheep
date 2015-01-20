#encoding: utf-8
from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user,logout_user,login_required,current_user

from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms	import LoginForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm,\
	ChangeEmailForm

@auth.before_app_request
def before_request():
	if current_user.is_authenticated():
		current_user.ping()

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('错误的用户名或密码！')
	return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('你已经退出！')
	return redirect(url_for('main.index'))

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash('你的密码已经修改！')
			return redirect(url_for('main.index'))
		else:
			flash('错误的密码。')
	return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous():
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email,'重置密码','auth/email/reset_password',
				user=user,token=token,next=request.args.get('next'))
		flash('重置密码邮件已经发送到你的邮箱！')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html',form = form)

@auth.route('/reset/<token>',methods=['GET',"POST"])
def password_reset(token):
	if not current_user.is_anonymous():
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token,form.password.data):
			flash('你的密码已经修改！')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html',form = form)

@auth.route('/change-email',methods=['GET','POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email,'确认你的邮箱','auth/email/change_email',
				user=current_user,token=token)
			flash('确认你新邮箱的邮件已经发送！')
			return redirect(url_for('main.index'))
		else:
			flash('错误的邮箱或密码！')
	return render_template('auth/change_email.html',form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('你的邮箱已经更改！')
	else:
		flash('错误的请求！')
	return redirect(url_for('main.index'))






			