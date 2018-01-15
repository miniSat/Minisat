from django.views.generic import TemplateView
import docker
import os
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
    Operating_system_model,
    Create_host_model
)
from main_app.modules import vm_manage as vm


# Create your views here.

def home(request):
    return render(request, 'home.html')


def compute_resource(request):
    form = Compute_resource_form()
    compute_resource_list = Compute_resource_model.objects.all()
    return render(request, 'infrastructure/compute_resource.html',
                  {'title_name': 'Create New Compute Resource', 'form': form,
                   'compute_obj': compute_resource_list})


def post_data(request):
    form = Compute_resource_form(request.POST)
    if form.is_valid():
        getssh = "sshpass -p " + form.cleaned_data["root_password"] + " ssh-copy-id root@" + form.cleaned_data[
            "ip_address"] + ' -o "StrictHostKeyChecking no" '
        os.system(getssh)
        compute = Compute_resource_model(
            name=form.cleaned_data["name"],
            ip_address=form.cleaned_data["ip_address"],
            root_password=form.cleaned_data["root_password"]
        )
        compute.save()
    return HttpResponseRedirect('/')


def profile(request):
    form = Profile_form()
    profile_list = Profile_model.objects.all()
    return render(request, 'infrastructure/profile.html',
                  {'title_name': 'Profile', 'form': form, 'profile_obj': profile_list})


def post_profile(request):
    form = Profile_form(request.POST)
    if form.is_valid():
        profile = Profile_model(
            profile_name=form.cleaned_data["profile_name"],
            ram=form.cleaned_data["ram"],
            cpus=form.cleaned_data["cpus"],
            disk_size=form.cleaned_data["disk_size"]
        )
        profile.save()
    return HttpResponseRedirect('/')


def create_host(request):
    form = Create_host_form()
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    compute_name = list(zip(compute_name, compute_name))
    profile_name = Profile_model.objects.values_list("profile_name", flat=True)
    profile_name = list(zip(profile_name, profile_name))
    os_name = Operating_system_model.objects.values_list("os_name", flat=True)
    os_name = list(zip(os_name, os_name))
    return render(request, 'host/create_host.html',
                  {'title_name': 'Create A New Host', 'form': form, 'os_name': os_name, 'compute_name': compute_name,
                   'profile_name': profile_name})


def operating_system(request):
    form = Operating_system_form()
    operating_system_list = Operating_system_model.objects.all()
    return render(request, 'host/operating_system.html',
                  {'title_name': 'Add Operating System', 'form': form, 'os_obj': operating_system_list})


def post_operating_system(request):
    form = Operating_system_form(request.POST)
    if form.is_valid():
        operating_sys = Operating_system_model(
            os_name=form.cleaned_data["os_name"],
            os_location=form.cleaned_data["os_location"]
        )
        operating_sys.save()
    return HttpResponseRedirect('/')


def post_create_host(request):
    form = Create_host_form(request.POST)
    if form.is_valid():
        create_host = Create_host_model(
            vm_name=form.data['vm_name'],
            vm_os=form.data['vm_os'],
            select_vm_profile=form.data['select_vm_profile'],
            select_compute=form.data['select_compute']
        )
        # '''
        form_profile = form.cleaned_data['select_vm_profile']
        form_compute = form.cleaned_data['select_compute']
        profile_details = list(
            Profile_model.objects.filter(profile_name=create_host.select_vm_profile).values_list()[0])
        *not_imp1, ram, cpus, disk_size = profile_details

        compute_details = list(Compute_resource_model.objects.filter(name=create_host.select_compute).values_list()[0])
        *not_imp2, compute_ip, compute_passwd = compute_details

        os_details = list(Operating_system_model.objects.filter(os_name=create_host.vm_os).values_list()[0])
        *not_imp3, location_url = os_details
        # final_cmd = 'virt-install --connect qemu+ssh://root@'+compute_ip+'/system --name '+form_vm+' --ram '+str(ram) \
        #            + ' --vcpus '+str(cpus)+' --disk path=/var/lib/libvirt/images/'+form_vm+'.qcow2,bus=virtio,size='+str(disk_size)+' --location '+location_url+' --network bridge:virbr0 &'
        # os.system(final_cmd)

        # print(compute_ip, create_host.vm_name, ram, cpus, disk_size, location_url)
        # print(create_host.select_vm_profile, create_host.vm_name, create_host.vm_os, create_host.select_compute)

        vm.vm_create(compute_ip, create_host.vm_name, ram, cpus, disk_size, location_url)
        create_host.save()
    return HttpResponseRedirect('/')


def new_container(request):
    form = newContainerform
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    compute_name = list(zip(compute_name, compute_name))
    return render(request, 'containers/new_container.html', {'title_name': "New Container", 'form': form, 'compute_name':compute_name})


def post_new_container(request):
    form = newContainerform(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect('/')


def local_images(request):
    form = Local_image_form
    images_list = {}
    client = docker.from_env()
    for i in range(0, len(client.images.list())):
        image = client.images.list()[i]
        images_list[image.attrs["Id"].split(":")[1][:10]] = [
            image.attrs["RepoTags"][0].split(":")[0],
            image.attrs["RepoTags"][0].split(":")[1],
            str(image.attrs["Size"])[:-6],
            image.attrs["Created"].split("T")[0]
        ]
    return render(request, 'containers/local_images.html',
                  {'title_name': "Local Docker Images", "images_list": images_list, 'form': form})


def post_docker_image(request):
    client = docker.from_env()
    form = Local_image_form(request.POST)
    if form.is_valid():
        docker_text = form.cleaned_data['dockerfile']
        image_name = form.cleaned_data['image_name'] + ":" + form.cleaned_data['tag_name']
        with open(os.path.join("main_app/templates/containers", "Dockerfile"), "w") as fobj:
            fobj.write(docker_text)
        client.images.build(path="main_app/templates/containers/", tag=image_name)
    return HttpResponseRedirect('/')
