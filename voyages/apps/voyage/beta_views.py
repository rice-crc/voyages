from django.shortcuts import render

def search_view(request):
    return render(request, 'voyage/beta_search_main.html')