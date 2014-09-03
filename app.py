## -*- coding: utf-8 -*-
import imp
from os.path import join, dirname, basename
from glob import glob
from simpleweb import controller, template

try:
    from google.appengine.ext.webapp.util import run_wsgi_app
except ImportError:
    running_from_gae = False
else:
    running_from_gae = True

current_dir = dirname(__file__)


# Set a default app root handler, to bind controllers until we find an "index" controller
class AppServerRoot(object):  # Application Server Root place holder

    def index(self):
        pass


controller.set_default_config(AppServerRoot())
application = controller.application()

# Setup template lookup directories
template.set_directories([join(current_dir, 'views')])

# Load and setup controllers
for controller_file in glob(join(current_dir, 'controllers', '*.py')):
    module_name = 'simpleweb.controllers.'+basename(controller_file)
    imp.load_source(module_name, controller_file)

# Setup static file serve handling for 'static' sub-dirs
for static_dir in glob(join(current_dir, 'static', '*')):
    conf = {}
    conf['/'+basename(static_dir)] ={ 'tools.staticdir.dir': static_dir,
        'tools.staticdir.on': True
        }
    application.merge(conf)

if running_from_gae:
    run_wsgi_app(application)
else:
    controller.quickstart(AppServerRoot())



