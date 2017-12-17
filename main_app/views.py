from django.views.generic import TemplateView
from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'home.html')

def compute_resource(request):
    return render(request,'compute_resource.html',{'title_name':'Create New Compute Resource'})
