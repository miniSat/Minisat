from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import (
                    Compute_resource_form,
                    Create_host_form,
                    Profile_form,
                    Operating_system_form
                    )
from django.http import (
                         HttpResponseRedirect,
                         HttpResponse
                         )
from .models import (
                    Compute_resource_model,
                    Profile_model,
                    Operating_system_model
                    )


# Create your views here.

def home(request):
    return render(request, 'home.html')


def compute_resource(request):
    form = Compute_resource_form()
    compute_resource_list = Compute_resource_model.objects.all()
    return render(request, 'compute_resource.html', {'title_name': 'Create New Compute Resource', 'form': form, 'compute_obj':compute_resource_list})


def post_data(request):
    form = Compute_resource_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def profile(request):
    form = Profile_form()
    return render(request, 'profile.html', {'title_name': 'Profile', 'form': form})


def post_profile(request):
    form = Profile_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def create_host(request):
    form = Create_host_form()
    return render(request, 'create_host.html', {'title_name': 'Create A New Host', 'form': form})


def operating_system(request):
    form = Operating_system_form()
    return render(request, 'operating_system.html', {'title_name':'Add Operating System', 'form':form})


def post_operating_system(request):
    form = Operating_system_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def post_create_host(request):
    form = Create_host_form(request.POST)
    if form.is_valid():
        form_vm = form.cleaned_data['vm_name']
        form_os = form.cleaned_data['vm_os']
        form_profile = form.cleaned_data['select_vm_profile']
        profile_details = list(Profile_model.objects.filter(profile_name=form_profile).values_list()[0])
        *not_imp1, ram, cpus, disk_size, compute_profile = profile_details
        compute_details = list(Compute_resource_model.objects.filter(name=compute_profile).values_list()[0])
        *not_imp2, compute_ip, compute_passwd = compute_details
        os_details = list(Operating_system_model.objects.filter(os_name=form_os).values_list()[0])
        *not_imp3, location_url = os_details
        final_cmd = 'virt-install --connect qemu+ssh://root@'+compute_ip+'/system --name '+form_vm+' --ram '+str(ram) \
                   + '--vcpus '+str(cpus)+' --disk path=/var/lib/libvirt/images/'+form_vm+'.qcow2,bus=virtio,size='+str(disk_size)+' --location '+location_url+' --network bridge:virbr0'
    return render(request, 'create_host.html', {'final_cmd': final_cmd})



