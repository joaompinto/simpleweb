# -*- coding: utf-8 -*-
import sys
import time
import cgi
import urllib
from xml.dom.minidom import parseString
from simpleweb import controller

if not 'simpleweb' in sys.path:
    sys.path.insert(0, 'simpleweb')
from mako.lookup import TemplateLookup
from dominate.tags import *
sys.path.pop(0)

def set_directories(templates_directories):
    """
    Sets the following configuration directories:
        templates_directories - list of dirs to lookup for templates
    module_directory - directory to keep cached template modules
    """
    global _template_lookup
    if not '_template_lookup' in globals():
        _template_lookup = None

    # Template rendering with internationalization support
    _template_lookup = TemplateLookup(directories=templates_directories
                                      , input_encoding='utf-8'
                                      , output_encoding='utf-8'
                                      , encoding_errors='replace'
                                      , strict_undefined=True
                                      , default_filters=['strip_none', 'h']
                                      , imports=['from simpleweb.template import strip_none, html_lines, quote']
    )

def build_simple_form(form_xml):
    dom = parseString(form_xml)
    assert dom.documentElement.tagName == "simpleform"
    new_form = form(role='form', method='post')
    with new_form:
        for element in dom.getElementsByTagName('input'):
            with div(_class="form-group row"):
                with div(_class="col-xs-%i" % int(element.getAttribute('view_size'))):
                    if element.getAttribute('type') == "submit":
                        button(element.getAttribute('label'))
                    else:
                        if element.getAttribute('label'):
                            label(element.getAttribute('label'))
                            kwargs = {'_class': 'form-control'}
                            args = ['type', 'name', 'placeholder']
                            if element.getAttribute('required') == "1":
                                args.append('required')
                            for kw in args:
                                kwargs[kw] = element.getAttribute(kw)
                            input(**kwargs)
    return unicode(new_form)


def render(template_name, **kwargs):
    global _template_lookup

    mytemplate = _template_lookup.get_template(template_name)

    # Inject herlper functions
    kwargs['build_simple_form'] = build_simple_form

    # Inject custom helper variables
    kwargs["controller_path"] = controller.controller_path()
    kwargs["controller_url"] = controller.controller_url()

    start_t = time.time()
    template_output = mytemplate.render(**kwargs)
    stop_t = time.time()
    if not template_name.endswith('.mail'):
        template_output += '\n<!-- Template %s rendering took %0.3f ms -->\n' % \
                           (template_name, (stop_t - start_t) * 1000.0)
    return template_output


def get_template_def(templatename, defname):
    global _template_lookup
    mytemplate = _template_lookup.get_template(templatename)
    return mytemplate.get_def(defname).render()


"""
   The following are global variables extending the mako templates
"""


def pagename():
    """
    """
    page_parts = cherrypy.request.path_info.strip("/").split("/")
    if not page_parts:
        return None
    pagename = page_parts[0]
    # if pagename= "" and len(path_parts)>1:
    # pagename = path_parts[len(path_parts) - 2]
    return pagename


# Because the unicode filter returns "None" for None strings
# We want to return '' for those
def strip_none(text):
    if text is None:
        return ''
    else:
        return unicode(text)


def html_lines(text):
    if text is None:
        return ''
    else:
        text = cgi.escape(unicode(text), True)
        return text.replace('\n', '<br>')


def quote(text):
    return urllib.quote(text.decode('utf-8'))