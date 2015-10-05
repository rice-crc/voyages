import django

def set_language(request, lang_code):
    """
    A wrapper around django.views.i18n.set_language suitable for an AJAX GET request.
    :param request: web request.
    :param lang_code: language code of the new language to use site-wise.
    :return: a plain text response with the given lang_code.
    """
    request.method = 'POST'
    request.POST = {'language': lang_code}
    django.views.i18n.set_language(request)
    return django.http.HttpResponse(lang_code, content_type="text/plain")