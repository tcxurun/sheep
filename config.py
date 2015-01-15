import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SHEEP_MAIL_SUBJECT_PREFIX = ['Sheep']
	SHEEP_MAIL_SENDER = 'Sheep Admin <tcxurun@gmail.com>'
	SHEEP_ADMIN = os.environ.get('SHEEP_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep_dev"

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep_test"

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep"

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
