import imp
from os.path import join, dirname, basename
from glob import glob

running_from_gae = True
try:
    from google.appengine.ext.webapp.util import run_wsgi_app
except ImportError:
    running_from_gae = False


current_dir = dirname(__file__)

from simpleweb import controller, template

class AppServerRoot(object):  # Application Server Root place holder

    def index(self):
        pass

# Load and setup controllers
controller.root = AppServerRoot()
for controller_file in glob(join(current_dir, 'controllers', '*.py')):
    module_name = 'simpleweb.controllers.'+basename(controller_file)
    imp.load_source(module_name, controller_file)

application = controller.application()


# Setup template directories
template.set_directories([join(current_dir, 'views')])

# Setup static contents directories for file serving
static_dirs = ['components', 'css']
for static_dir in static_dirs:
    controller.add_static_dir(application, static_dir, join(current_dir, static_dir))

if running_from_gae:
    run_wsgi_app(application)
else:
    controller.quickstart(AppServerRoot())



