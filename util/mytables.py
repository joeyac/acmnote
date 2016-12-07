# coding: utf-8
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape

from table.utils import Accessor
from table.columns import Column
from django.utils import timezone


class MyLinkColumn(Column):
    def __init__(self, header=None, links=None, delimiter='&nbsp', field=None, **kwargs):
        self.links = links
        self.delimiter = delimiter
        kwargs['safe'] = False
        super(MyLinkColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):

        print(link.render(obj) for link in self.links)
        return self.delimiter.join([link.render(obj) for link in self.links])


class MyDateTimeColumn(Column):

    DEFAULT_FORMAT = "%Y-%m-%d %H:%I:%S"

    def __init__(self, field, header=None, format=None, **kwargs):
        self.format = format or MyDateTimeColumn.DEFAULT_FORMAT
        super(MyDateTimeColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        datetime = Accessor(self.field).resolve(obj)
        # print(datetime)
        datetime = timezone.localtime(datetime)
        # print(datetime)
        text = datetime.strftime(self.format)
        return escape(text)


class MyLink(object):
    """
    Represents a html <a> tag.
    """
    def __init__(self, field=None, text=None, viewname=None, args=None, kwargs=None, urlconf=None,
                 current_app=None, attrs=None):
        self.basetext = text
        self.viewname = viewname
        self.args = args or []
        self.kwargs = kwargs or {}
        self.urlconf = urlconf
        self.current_app = current_app
        self.base_attrs = attrs or {}
        self.field = field

    @property
    def text(self):
        if self.field:
            basetext = Accessor(self.field).resolve(self.obj)
        else:
            basetext = self.basetext
        return escape(basetext)

    @property
    def url(self):
        if self.viewname is None:
            return ""

        # The following params + if statements create optional arguments to
        # pass to Django's reverse() function.
        params = {}
        if self.args:
            params['args'] = [arg.resolve(self.obj)
                              if isinstance(arg, Accessor) else arg
                              for arg in self.args]
        if self.kwargs:
            params['kwargs'] = {}
            for key, value in self.kwargs.items():
                params['kwargs'][key] = (value.resolve(self.obj)
                                         if isinstance(value, Accessor) else value)
        if self.urlconf:
            params['urlconf'] = (self.urlconf.resolve(self.obj)
                                 if isinstance(self.urlconf, Accessor)
                                 else self.urlconf)
        if self.current_app:
            params['current_app'] = (self.current_app.resolve(self.obj)
                                     if isinstance(self.current_app, Accessor)
                                     else self.current_app)

        # print(reverse(self.viewname, **params))
        return reverse(self.viewname, **params)

    @property
    def attrs(self):
        if self.url:
            self.base_attrs["href"] = self.url
        return self.base_attrs

    def render(self, obj):
        """ Render link as HTML output tag <a>.
        """
        self.obj = obj
        # print(self.attrs)
        attrs = ' '.join([
            '%s="%s"' % (attr_name, attr.resolve(obj))
            if isinstance(attr, Accessor)
            else '%s="%s"' % (attr_name, attr)
            for attr_name, attr in self.attrs.items()
        ])
        return mark_safe(u'<a %s>%s</a>' % (attrs, self.text))
