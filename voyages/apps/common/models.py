from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
class SavedQuery(models.Model):
    """
    Used to store a query for later use in a permanent link.
    """

    ID_LENGTH = 8

    # This is the short sequence of characters that will be used when repeating the query.
    id = models.CharField(max_length=ID_LENGTH, primary_key=True)
    # A hash string so that the query can be quickly located.
    hash = models.CharField(max_length=255, db_index=True, default='')
    # The actual query string.
    query = models.TextField()
    # Indicates whether this is a legacy query or a new JSON format query
    is_legacy = models.BooleanField(default=True)

    def get_link(self, request, url_name):
        """
        This method can be called directly in Views that need to have
        permanent linking functionality.
        :param request: The web request containing POST data that needs to be persisted.
        :param url_name: The URL name that is used to revert a permanent link URL as specified in the urls.py file.
        :return: A plain text response containing the link or an Http405 error.
        """
        self.query = request.POST.urlencode()
        self.save()
        from django.core.urlresolvers import reverse
        link = ('https://' if request.is_secure() else 'http://') + request.get_host() + \
               reverse(url_name, kwargs={'link_id': self.id})
        from django.http import HttpResponse
        return HttpResponse(link, content_type='text/plain')

    def get_post(self):
        """
        Parse the stored query string and return a dict which is compatible
        with the original post that generated the permalink.
        :return: dict with stored POST data.
        """
        from urlparse import parse_qs
        src = parse_qs(self.query, keep_blank_values=True)
        post = {}
        for name, value in src.items():
            # This is an ugly HACK to detect entries which should be lists
            # even though there is only one entry in said list.
            # The best way to handle the whole issue of permanent links would
            # be to implement a complete model of the search queries, which
            # could be persisted to the database in a structured format.
            # At this point, though the options are somewhat limited.
            if len(value) == 1 and 'choice_field' not in name and 'select' not in name:
                post[name] = value[0]
            else:
                post[name] = value
        return post

    def save(self, *args, **kwargs):
        import hashlib
        hash_object = hashlib.sha1(self.query)
        self.hash = hash_object.hexdigest()
        pre_existing = list(SavedQuery.objects.filter(hash=self.hash).filter(query=self.query))
        if len(pre_existing) > 0:
            self.id = pre_existing[0].id
        else:
            import random
            import string
            self.id = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                range(self.ID_LENGTH))
            super(SavedQuery, self).save(*args, **kwargs)

    @classmethod
    def restore_link(cls, link_id, session, session_key, redirect_url_name):
        """
        Fetch the given link_id post data and set session[session_key]
        with the POST dict. Then redirect the page to the URL identified
        by redirect_url_name.
        If the link_id is not found, return Http404
        :param link_id: The id of the link.
        :param session: The web session.
        :param session_key: The key that will be used to set the restored POST data to the session.
        :param redirect_url_name: The name of the redirect url as in urls.py.
        :return: A redirect response to the appropriate page or an Http404 exception.
        """
        permalink = get_object_or_404(SavedQuery, pk=link_id)
        # Save the query in the session and redirect.
        session[session_key] = permalink.get_post()
        from django.http import HttpResponseRedirect
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse(redirect_url_name))

def get_pks_from_haystack_results(results):
    """
    This is a HACK that gives us much better performance when enumerating the
    voyage primary keys of the search results.
    :param results:
    :return:
    """
    q = results.query._clone()
    q._reset()
    q.set_limits(0, 500000)
    final_query = q.build_query()
    search_kwargs = q.build_params(None)
    search_kwargs['fields'] = 'id'
    search_kwargs = q.backend.build_search_kwargs(final_query, **search_kwargs)
    try:
        raw_results = q.backend.conn.search(final_query, **search_kwargs)
    except:
        raw_results = []
    return [int(x['id'].split('.')[-1]) for x in raw_results]

def get_values_from_haystack_results(results, fields):
    """
    Retrieves a set of fields from haystack search results in
    RAW format. This is useful to bypass some slow methods in haystack.
    :param results:
    :param fields:
    :return:
    """
    q = results.query._clone()
    q._reset()
    q.set_limits(0, 500000)
    final_query = q.build_query()
    search_kwargs = q.build_params(None)
    search_kwargs['fields'] = fields
    search_kwargs = q.backend.build_search_kwargs(final_query, **search_kwargs)
    try:
        raw_results = q.backend.conn.search(final_query, **search_kwargs)
    except:
        raw_results = []
    return raw_results
