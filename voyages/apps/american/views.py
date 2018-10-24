from django.shortcuts import render

def index(request):
    return render(request, 'voyage/new-ui.html', {'mode' : 'intra'})