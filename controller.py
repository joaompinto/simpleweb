import cherrypy
root = None

def add_static_dir(application, static_dir, dir_name):

    conf = {}
    conf['/'+static_dir] ={ 'tools.staticdir.dir': dir_name,
        'tools.staticdir.on': True
        }
    application.merge(conf)


def attach(controller_obj, controller_path_name):
    global root
    controller_path_name = controller_path_name.strip("/")
    if controller_path_name == '':  # No path provided, override the index handler
        root.index = controller_obj.index
    else:
        setattr(root, controller_path_name, controller_obj)

def publish(func=None, *args):
    return cherrypy.expose(func, *args)
