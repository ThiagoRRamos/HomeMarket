from django.shortcuts import render
from marketapp.models import Supermercado


def home(request):
    supermercados = Supermercado.objects.all()
    return render(request, 'home.html', {'supermercados': supermercados})
