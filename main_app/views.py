from django.views.generic import TemplateView
import docker, os
from django.shortcuts import render
from .forms import (
                    Compute_resource_form,
                    Create_host_form,
                    Profile_form,
                    Operating_system_form,
                    newContainerform,
                    Local_image_form
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
    return render(request, 'infrastructure/compute_resource.html', {'title_name': 'Create New Compute Resource', 'form': form,
                                                     'compute_obj': compute_resource_list})


def post_data(request):
    form = Compute_resource_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def profile(request):
    form = Profile_form()
    profile_list = Profile_model.objects.all()
    return render(request, 'infrastructure/profile.html', {'title_name': 'Profile', 'form': form, 'profile_obj': profile_list})


def post_profile(request):
    form = Profile_form(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def create_host(request):
    form = Create_host_form()
    return render(request, 'host/create_host.html', {'title_name': 'Create A New Host', 'form': form})


def operating_system(request):
    form = Operating_system_form()
    operating_system_list = Operating_system_model.objects.all()
    return render(request, 'host/operating_system.html', {'title_name': 'Add Operating System', 'form': form, 'os_obj': operating_system_list})


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
                   + ' --vcpus '+str(cpus)+' --disk path=/var/lib/libvirt/images/'+form_vm+'.qcow2,bus=virtio,size='+str(disk_size)+' --location '+location_url+' --network bridge:virbr0'
    return render(request, 'create_host.html', {'final_cmd': final_cmd})


def new_container(request):
    form = newContainerform
    return render(request, 'containers/new_container.html', {'title_name':"New Container", 'form':form})


def post_new_container(request):
    form = newContainerform(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def local_images(request):
    form = Local_image_form
    images_list = {}
    client = docker.from_env()
    for i in range(0,len(client.images.list())):
        image = client.images.list()[i]
        images_list[image.attrs["Id"].split(":")[1][:10]] = [
            image.attrs["RepoTags"][0].split(":")[0],
            image.attrs["RepoTags"][0].split(":")[1],
            str(image.attrs["Size"])[:-6],
            image.attrs["Created"].split("T")[0]
        ]
    print(images_list)
    return render(request, 'containers/local_images.html', {'title_name': "Local Docker Images", "images_list":images_list, 'form':form})


def post_docker_image(request):
    client = docker.from_env()
    form = Local_image_form(request.POST)
    if form.is_valid():
        docker_text = form.cleaned_data['dockerfile']
        image_name = form.cleaned_data['image_name']+":"+form.cleaned_data['tag_name']
        with open(os.path.join("main_app/templates/containers", "Dockerfile"),"w") as fobj:
            fobj.write(docker_text)
        client.images.build(path="main_app/templates/containers/", tag=image_name)
    return HttpResponseRedirect('/')