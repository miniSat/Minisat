from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import (
                    compute_resource_form,
                    create_host_form,
                    profile_form
                    )
from django.http import HttpResponseRedirect,HttpResponse
from .models import Compute_resource_model,Profile_model


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

def create_host(request):
    form = create_host_form()
    return render(request,'create_host.html', {'title_name':'Create A New Host','form':form})

def post_create_host(request):
    form = create_host_form(request.POST)
    if form.is_valid():
        form_vm = form.cleaned_data['vm_name']
        form_os = form.cleaned_data['vm_os']
        form_profile = form.cleaned_data['select_vm_profile']
        profile_details = list(Profile_model.objects.filter(profile_name=form_profile).values_list()[0])
        *not_imp1,ram,cpus,disk_size,compute_profile=profile_details
        compute_details = list(Compute_resource_model.objects.filter(name=compute_profile).values_list()[0])
        *not_imp2,compute_ip,compute_passwd=compute_details
        final_cmd = 'virt-install --connect qemu+ssh://root@'+compute_ip+'/system --name '+form_vm+' --ram '+str(ram)+' --vcpus '+str(cpus)+' --disk path=/var/lib/libvirt/images/'+form_vm+'.qcow2,bus=virtio,size='+str(disk_size)+' --network bridge:virbr0'
    return render(request,'create_host.html',{'final_cmd':final_cmd})

