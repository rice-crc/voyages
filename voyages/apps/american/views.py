from django.shortcuts import render

def index(request):
    return render(request, 'voyage/database.html', {'mode' : 'intra'})