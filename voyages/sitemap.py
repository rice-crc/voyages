from django.conf import settings
import datetime
import os
import stat
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
import posixpath
import urllib

class ViewSitemap(Sitemap):
   # Reverse static views for XML sitemap.
    def __init__(self):
        self._items = ['index', 'voyage:guide', 'voyage:search', ]
   
    def items(self):
    # Return list of url names for views to include in sitemap
        return self._items

    def location(self, item):
        return reverse(item)

# Example usage, a Sitemap class
class StaticSitemap(Sitemap):
    """Return the static sitemap items"""
    priority = 0.5
    changefreq = 'monthly'

    def __init__(self, patterns):
        self._items = {}
        self._initialize(patterns)

    def _initialize(self, patterns):
        do_not_show = []
        for p in patterns:
            if getattr(p,'url_patterns',False):
               for q in p.url_patterns:
                   # urls.py in other apps
               
                   if [url for url in do_not_show if url in q.regex.pattern]:
                       # do not show urls with this word in them
                       continue
                   if q.regex.groups:
                       continue
                   if (hasattr(q, 'default_args') and ('template_name' in q.default_args or 'template' in q.default_args)) or\
                           (hasattr(q, 'default_kwargs') and ('template_name' in q.default_kwargs or 'template' in q.default_kwargs)):
                       # only urls with templates, because we get mtime from the file
                       if getattr(q,'name',False):
                           # only views with names so reverse() can work on them
                           self._items[p.namespace + ':' + q.name] = self._get_modification_date(q, p.namespace)
            else:
                if [url for url in do_not_show if url in p.regex.pattern]:
                # do not show urls with this word in them
                    continue
                if p.regex.groups:
                    continue
                if 'template_name' in p.default_args or 'template' in p.default_args :
                    # only urls with templates, because we get mtime from the file
                    if getattr(p,'name',False):
                        # only views with names so reverse() can work on them
                        self._items[p.name] = self._get_modification_date(p, '')

    def _get_modification_date(self, p, appname):
        # We get the modification date from the template itself
        if getattr(p,'default_args',None):
            if 'template_name' in p.default_args:
                template = p.default_args['template_name']
            elif 'template' in p.default_args:
                template = p.default_args['template']
            template_path = self._get_template_path(template, appname)
            
            if template_path == None :
                return datetime.datetime.now()
            else:
                mtime = os.stat(template_path).st_mtime
                return datetime.datetime.fromtimestamp(mtime)

    def _get_template_path(self, template_path, appname):
        # check the app directory
        path = settings.BASE_DIR + '/apps/' + appname + '/templates/' + template_path
        if os.path.exists(path) :
            return path
        
        for template_dir in settings.TEMPLATES[0]['DIRS']:
            path = os.path.join(template_dir, template_path)
            if os.path.exists(path):
                return path
        return None

    def items(self):
        return self._items.keys()

    def lastmod(self, obj):
        return self._items[obj]

    def location(self, obj):
        return reverse(obj)
