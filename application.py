## -*- coding: utf-8 -*-
import imp
import sys
from os.path import join, basename
from simpleweb import controller, template
from glob import glob

if not 'simpleweb' in sys.path:
    sys.path.insert(0, 'simpleweb')
#if not 'cherrypy' in sys.modules:
f, filename, desc = imp.find_module('cherrypy', ['simpleweb'])
cherrypy = imp.load_module('cherrypy', f, filename, desc)


wsgi_app = None

# Set a default app root handler, to bind controllers until we find an "index" controller
class AppServerRoot(object):  # Application Server Root place holder

    def index(self):
        pass

def set_template_dirs(template_dirs):
    template.set_directories(template_dirs)

def set_default_config():
    global wsgi_app

    # Enforce utf8 encoding
    cherrypy.config.update({'tools.encode.on': True
        , 'tools.encode.encoding': 'utf-8'
        , 'tools.encode.errors': 'replace'
    })
    controller.app_root = AppServerRoot()

    wsgi_app = cherrypy.tree.mount(controller.app_root, '/')


# Load and setup controllers
def load_controllers(controller_dir):
    global wsgi_app
    for controller_file in glob(join(controller_dir, '*.py')):
        module_name = 'simpleweb.controllers.'+basename(controller_file)
        imp.load_source(module_name, controller_file)


# Setup static file serve handling for 'static' sub-dirs
def set_static_dirs(static_dir):
    global wsgi_app
    for static_dir in glob(join(static_dir, '*')):
        conf = {}
        conf['/'+basename(static_dir)] ={ 'tools.staticdir.dir': static_dir,
            'tools.staticdir.on': True
            }
        wsgi_app.merge(conf)
