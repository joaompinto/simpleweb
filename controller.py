import cherrypy
root = None

def add_static_dir(application, static_dir, dir_name):

    conf = {}
    conf['/'+static_dir] ={ 'tools.staticdir.dir': dir_name,
        'tools.staticdir.on': True
        }
    application.merge(conf)


def attach(controller_path_name, controller_obj,):
    global root
    controller_path_name = controller_path_name.strip("/")
    if controller_path_name == '':  # No path provided, override the index handler
        root.index = controller_obj.index
    else:
        setattr(root, controller_path_name, controller_obj)


def publish(func=None, *args):
    return cherrypy.expose(func, *args)


def get_cookie(name, default=None):
    return cherrypy.request.cookie.get(name, default)


def set_cookie(name, value, path='/', max_age=3600, version=1):
    cookie = cherrypy.response.cookie
    cookie[name] = value
    cookie[name]['path'] = path
    cookie[name]['max-age'] = max_age
    cookie[name]['version'] = version


def delete_cookie(name):
    cherrypy.response.cookie[name] = 'deleting'
    cherrypy.response.cookie[name]['expires'] = 0

def method():
    return cherrypy.request.method

def params()    :
    return cherrypy.request.params