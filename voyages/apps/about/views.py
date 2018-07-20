from voyages.apps.common.views import render_locale_flatpage

def render_about_flatpage(request, flatpage_url):
    """
    Renders flat pages using the default template for About pages.
    """
    return render_locale_flatpage(request, 'about/flatpage.html', flatpage_url)