# -*- coding: utf-8 -*-
'''
Created on 2009-12-18

function found at: http://www.djangosnippets.org/snippets/1627/
'''
def easy_tag(func):
    """
    deal with the repetitive parts of parsing template tags
    
    http://www.djangosnippets.org/snippets/1627/
    """
    def inner(parser, token):
        #print token
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner
