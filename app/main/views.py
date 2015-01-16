from datetime import datetime
from flask import render_template,session,redirect,url_for,request,flash,current_app
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from .forms import PostForm
from ..models import User,Post

@main.route('/',methods=['GET','POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data)
		db.session.add(post)
		return redirect(url_for('.index()'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',form=form,posts=posts)




main.route('edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated')
		return redirect(url_for('.post',id=post.id))
	form.body.data = post.body
	return render_template('edit_post.html',form=form)
