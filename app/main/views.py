#encoding: utf-8
from datetime import datetime
from flask import render_template,session,redirect,url_for,request,flash,current_app
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from .forms import PostForm,CommentForm,EditProfileForm
from ..models import User,Post,Comment

@main.route('/',methods=['GET','POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data)
		db.session.add(post)
		return redirect(url_for('.index'))
	page = request.args.get('page',1,type=int)

	query = Post.query
	pagination = query.order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['SHEEP_POSTS_PER_PAGE'],error_out=False)

	posts = pagination.items

	return render_template('index.html',form=form,posts=posts,pagination=pagination)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(request.form)
	if form.validate_on_submit():
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('你的介绍已经更新!')
		return redirect(url_for('.edit_profile',about_me=current_user.about_me))
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html',form=form)

@main.route('/view-profile',methods=['GET','POST'])
def view_profile():
	form = EditProfileForm()
	user = User.query.first()
	form.about_me.data = user.about_me
	return render_template('view_profile.html',form=form,user=user)

@main.route('/post',methods=['GET','POST'])
@login_required
def post():
	form = PostForm(request.form)
	#if form.validate_on_submit():
	print 'title: %s' %form.title.data
	print 'body: %s' % form.body.data
	print 'post: %s' %request.method
	print 'validate: %s' %form.validate()
	print 'validate_on_submit:%s' % form.validate_on_submit()
	print 'errors:%s' % form.errors
	if request.method == 'POST' and form.validate_on_submit():
		post = Post(title=form.title.data,body=form.body.data)
		db.session.add(post)
		return redirect(url_for('.index'))
	#form.title.data = ''
	#form.body.data = ''
	flash('标题和正文为必填项！')
	return render_template('post.html',form=form)

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated')
		return redirect(url_for('.post',id=post.id))
	form.title.data = post.title
	form.body.data = post.body
	return render_template('edit_post.html',form=form)

@main.route('/view/<int:id>',methods=['GET','POST'])
@login_required
def view(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	comments = post.comments
	if form.validate_on_submit():
		comment = Comment(nickname=form.nickname.data,body=form.body.data,
			post=post)
		db.session.add(comment)
		flash('您的评论已经提交！')
		url_for('.view',id=post.id)
	form.nickname.data = ''
	form.body.data = ''
	return render_template('view_post.html',post=post,comments=comments,form=form)


@main.route('/post/comment/<int:id>',methods=['GET','POST'])
def comment(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(nickname=form.nickname.data,body=form.body.data,
			post=post)
		db.session.add(comment)
		flash('您的评论已经提交！')
		return redirect(url_for('.comment',id=post.id,page=-1))
	page = request.args.get('page',1,type=int)
	print 'before page: %s' % page
	if page == -1:
		page=(post.comments.count() -1) / \
			current_app.config['SHEEP_POSTS_PER_PAGE'] + 1
	print 'page: %s' % page
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
		page,per_page=current_app.config['SHEEP_POSTS_PER_PAGE'],error_out=False)
	comments = pagination.items
	return render_template('view_post.html',post=post,form=form,comments=comments,pagination=pagination)

@main.route('/moderate')
@login_required
def moderate():
	page = request.args.get('page',1,type=int)
	pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
		page,per_page=current_app.config['SHEEP_POSTS_PER_PAGE'],error_out=False)
	comments = pagination.items
	return render_template('moderate.html',comments=comments,pagination=pagination,page=page)

@main.route('/moderate/enable/<int:id>')
@login_required
def moderate_enable(id):
	comment = Comment.query.get_or_404(id)
	comment.disabled = False
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
def moderate_disable(id):
	comment = Comment.query.get_or_404(id)
	comment.disabled = True
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/archive')
def archive():
	page = request.args.get('page',1,type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['SHEEP_ARCHIVE_PER_PAGE'],error_out=False)
	posts = pagination.items
	return render_template('archive.html',posts=posts,pagination=pagination,page=page)

