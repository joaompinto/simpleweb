import sys
import imp
from os.path import join, dirname, basename
from glob import glob

current_dir = dirname(__file__)
sys.path.append(join(current_dir, 'simpleweb'))

import cherrypy
from simpleweb import controller, template

class AppServerRoot(object):  # Application Server Root place holder

    def index(self):
        pass

# Load and setup controllers
controller.root = AppServerRoot()
for controller_file in glob(join(current_dir, 'controllers', '*.py')):
    module_name = 'simpleweb.controllers.'+basename(controller_file)
    imp.load_source(module_name, controller_file)

application = cherrypy.tree.mount(controller.root, '/')

# Setup template directories
template.set_directories([join(current_dir, 'views')])

# Setup static contents directories for file serving
static_dirs = ['components']
for static_dir in static_dirs:
    controller.add_static_dir(application, static_dir, join(current_dir, static_dir))


