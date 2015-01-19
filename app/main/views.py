#encoding: utf-8
from datetime import datetime
from flask import render_template,session,redirect,url_for,request,flash,current_app
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from .forms import PostForm,CommentForm
from ..models import User,Post

@main.route('/',methods=['GET','POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data)
		db.session.add(post)
		return redirect(url_for('.index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',form=form,posts=posts)


@main.route('/post',methods=['GET','POST'])
@login_required
def post():
	form = PostForm()
	if form.validate_on_submit():
		print 'title: %s' % form.title.data
		post = Post(title=form.title.data,body=form.body.data)
		db.session.add(post)
		return redirect(url_for('.index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',form=form,posts=posts)

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

@main.route('/post/comment/<int:id>',methods=['GET','POST'])
def comment(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(nickname=form.nickname.data,body=form.body.name,
			post=post)
		db.session.add(comment)
		flash('您的评论已经提交！')
		return redirect(url_for('.post',id=post.id,page=-1))
	page = request,args.get('page',1,type=int)
	if page == -1:
		page=(post.comments.count() -1) / \
			current_app.config['SHEEP_POSTS_PER_PAGE'] + 1
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
		page,per_page=current_app.config['SHEEP_POSTS_PER_PAGE'],error_out=False)
	comments = pagination.items
	return render_template('post.html',post=post,form=form,comments=comments,)