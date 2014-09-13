## -*- coding: utf-8 -*-
from os.path import join, dirname
from simpleweb import application
from google.appengine.ext.webapp.util import run_wsgi_app

current_dir = dirname(__file__)

application.set_default_config()
application.set_template_dirs([join(current_dir, 'views')])
application.load_controllers(join(current_dir, 'controllers'))
application.set_static_dirs(join(current_dir, 'static'))
app = application.wsgi_app

run_wsgi_app(app)


