# -*- coding: utf-8 -*-
'''
Created on 2009-12-09

@author: Marcin Biernat <biern.m@gmail.com>
'''
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from easy_tag import easy_tag

register = template.Library() 

@register.tag()
@easy_tag
def include_with(tag, template_name, *args):
    """
    Combines functionality of standard "include" and "with" tag.
        First argument is template to include, all kwargs are appended,
        all args without value are set to true. This makes it easier
        to use templates more like rendering functions.
    Example:
        include_with('test.html', size=3, short, x=some_var.y|cut:" ")
        is equivalent to:
        {% with 1 as short, 3 as size, some_var.y|cut:" " as x %}
            {% include 'test.html' %}
        {% endwith %}
    
    
    """
    kwargs = {}
    for item in args:
        if '=' in item:
            kwargs[item.split("=")[0].strip()] = item.split("=")[1].strip()
        else:
            kwargs[item.strip()] = "'1'"
    
    return IncludeWithNode(template_name, kwargs)

            
class IncludeWithNode(template.Node):
    def __init__(self, template_name, kwargs):
        self.template_name = template.Variable(template_name)
        self.kwargs = kwargs
    
    def render(self, context):
        template_name = self.template_name.resolve(context)
        t = template.loader.get_template(template_name)
        # Do not save resolved values into context directly, as it will affect 
        # resolving next ones and may cause unwanted behaviour in some cases.
        for k, v in self.kwargs.items():
            self.kwargs[k] = template.Variable(v).resolve(context)
        
        context.push()
        # Do not use context.update(context) here!
        for k, v in self.kwargs.items():
            context[k] = v
        rendered = t.render(context)
        context.pop()
        return rendered


@register.filter(name='pygmentize')
@stringfilter
def pygmentize(value, language=None):
    try:
        from pygments import highlight
        from pygments.lexers import guess_lexer, get_lexer_by_name
        from pygments.formatters import HtmlFormatter
    except ImportError:
        #TODO: Log no pygments installed
        return value
    
    formatter_options = dict(
        linenos='inline',
    )
    try:
        lexer = guess_lexer(value) if language is None else \
            get_lexer_by_name(language)
        return mark_safe(highlight(value, lexer, 
            HtmlFormatter(**formatter_options)))
    except Exception:
        #TODO: Log error
        return value
    
pygmentize.is_safe = False
