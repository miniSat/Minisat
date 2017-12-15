from django.views.generic import TemplateView
from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'home.html')
