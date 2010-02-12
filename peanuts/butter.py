# -*- coding: utf-8 -*-
'''
Created on 2010-02-12

@author: Marcin Biernat

This module contains a mix of a variety of useful shortcut functions intended 
 to use inside Django app, to make it even more tasty :-) 
'''

from copy import copy

def copy_generic_options(std_options, *remove, **extra):
    """ 
    Copies 'std_options' dict and alters it according to other args.
    Saves time in writing similar sets of options for generic views.
    All named args will update std_options dict.
    All positional ones indicate fields to remove.
    """
    if not remove: remove = []
    res = copy(std_options)
    res.update(extra)
    for item in remove:
        del res[item]
        
    return res


from django.template import RequestContext

def shorter_view(view):
    #TODO: Create a view generator that may use custom context_instance, 
    #      extra_context, app_name and other arguments.
    """
    Reduces amount of boilerplate code in view return values.
    A view in order to be compatible should return a following list/tuple:
    (template_name, [dictionary, [mimetype]]) or string template_name.
    All those values are then passed to render_to_response along 
    with RequestContext of original request. If returned type is 
    not a string / list / tuple, then the returned value is not changed at all.
    This allows all HttpResponse and others to pass through.
    """
    def new_view(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        #Place string in a tuple
        if type(result) == str: result = (result, )
        elif not type(result) in (list, tuple): 
            #Not what are we looking for so return it
            return result
        
        #Is iterable, so
        nkwargs = {
                   'template_name' : result[0], 
                   'context_instance' : RequestContext(request)
                   }
        if len(result) > 1:
            nkwargs['dictionary'] = result[1]
            if len(result) > 2:
                nkwargs['mimetype'] = result[2]
        
#        if(app_name):
#            nkwargs['app_name'] = app_name
        return render_to_response(**nkwargs)
        
    return new_view
