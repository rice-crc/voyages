from voyages.apps.common.views import render_locale_flatpage

# A catch all for URL matching
def render_about_flatpage(request, flatpage_url):
    flatpage_url = "/about/" + flatpage_url + "/"
    return render_locale_flatpage(request, 'about/flatpage.html', flatpage_url)