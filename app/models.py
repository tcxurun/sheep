from datetime import datetime
from flask import current_app,request,url_for
from flask.ext.login import UserMixin,AnonymousUserMixin
from . import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from app.exceptions import ValidationError
import bleach
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attibute')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	@staticmethod
	def generate_admin(name='admin',password='admin'):
		u = User(username=name,password=password)
		db.session.add(u)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def generate_reset_token(self,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'reset':self.id})

	def reset_password(self,token,new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

	def generate_email_change_token(self,new_email,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY',expiration])
		return s.dumps({'change_email':self.id,'new_email':new_email})

	def change_email(self,token):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('change_email') != self.id:
			return False
		new_email = data.get('new_email')
		if new_email is None:
			return False
		if self.query.filter_by(email=new_email).first() is not None:
			return False
		self.email = new_email
		db.session.add(self)
		return True

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	def generate_auth_token(self,expiration):
		s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
		return s.dumps({'id':self.id}).decode('ascii')

	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		return User.query.get(data['id'])

	def is_administrator(self):
		return True

	def __repr__(self):
		return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

	
class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)

	@staticmethod
	def generate_posts(count=10):
		for i in range(count):
			text = i * 1000
			p = Post(body=text)
			db.session.add(p)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
		'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul','h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, strip=True))

	def to_json(self):
		json_comment = {
			'url': url_for('api..get_comment',id=self.id,_external=True),
			'post': url_for('api.get.get_post',id=self.post_id,_external=True),
			'body': self.body,
			'body_html':self.body_html,
			'timestamp':self.timestamp
		}

	@staticmethod
	def from_json(json_post):
		body = json_post.get('body')
		if body is None or body == '':
			raise ValidationError('post does not have a body')
		return Post(body=body)