from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import compute_resource_form
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    return render(request, 'home.html')

def compute_resource(request):
    form = compute_resource_form()
    return render(request,'compute_resource.html',{'title_name':'Create New Compute Resource', 'form':form})

def post_data(request):
    form = compute_resource_form(request.POST)
    if form.is_valid():
        form.save(commit=True)

    return HttpResponseRedirect('/')