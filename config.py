import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SHEEP_MAIL_SUBJECT_PREFIX = '[Sheep]'
	SHEEP_MAIL_SENDER = 'Sheep Admin <tcxurun@163.com>'
	SHEEP_ADMIN = os.environ.get('SHEEP_ADMIN')
	SHEEP_POSTS_PER_PAGE = 10
	SHEEP_COMMENTS_PER_PAGE = 10
	SHEEP_ARCHIVE_PER_PAGE = 50

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep_dev"

class UnixConfig(DevelopmentConfig):
	@classmethod
	def init_app(cls,app):
		import logging
		from logging.handlers import SysLogHandler
		syslog_handler = SysLogHandler()
		syslog_handler.setLevel(logging.WARNING)
		app.logger.addHandler(syslog_handler)


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep_test"

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/sheep"

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': UnixConfig
}
