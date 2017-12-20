from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import compute_resource_form,profile_form
from django.http import HttpResponseRedirect
from .models import compute_resource_model


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


def profile(request):
    form = profile_form()
    return render(request,'profile.html',{'title_name':'Profile', 'form':form})

def post_profile(request):
    form = profile_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')
