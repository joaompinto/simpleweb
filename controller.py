import cherrypy
import re
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


def redirect(url):
    raise cherrypy.HTTPRedirect(url)


def get_cookie(name, default_value=None):
    def unescape(s):
        m = re.match(r'^"(.*)"$', s)
        s = m.group(1) if m else s
        return s.replace("\\\\", "\\")
    if cherrypy.request.cookie.has_key(name):
        return unescape(cherrypy.request.cookies[name]).decode('unicode-escape')
    else:
        return default_value

def set_cookie(name, value, path='/', max_age=3600, version=1):
    cookie = cherrypy.response.cookie
    cookie['xpto'] = 12
    cookie['xpto']['path'] = '/'
    cookie['xpto']['max-age'] = 9000
    cookie[name] = value.encode('unicode-escape')
    cookie[name]['path'] = path
    cookie[name]['max-age'] = max_age

def delete_cookie(name):
    cherrypy.response.cookie[name] = 'deleting'
    cherrypy.response.cookie[name]['expires'] = 0


def method():
    return cherrypy.request.method


def params()    :
    return cherrypy.request.params


def current_url():
    """
    @return: the current request url
    """
    return cherrypy.request.base
