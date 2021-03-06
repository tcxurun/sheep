#!/usr/bin/env python
import os
from app import create_app,db
from app.models import User,Post
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate,MigrateCommand
import flask_wtf

app = create_app(os.getenv('SHEEP_CONFIG') or 'default')
flask_wtf.CsrfProtect(app)
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
	return dict(app=app,db=db,User=User,Post=Post)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	import sys
	reload(sys)
	sys.setdefaultencoding("utf-8")
	manager.run()
