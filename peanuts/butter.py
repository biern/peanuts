# -*- coding: utf-8 -*-
'''
Created on 2010-02-12

@author: Marcin Biernat

This module contains a mix of variety of useful shortcut functions intended 
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

