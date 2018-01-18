from django.views.generic import TemplateView
import docker
import os
from django.db import IntegrityError
from django.shortcuts import render
from main_app.modules.docker_manage import make_connection
# We'll use render to display our templates.

from .forms import (
    # We need to import our forms to use it.
    Compute_resource_form,
    Create_host_form,
    Profile_form,
    Operating_system_form,
    newContainerform,
    Local_Images
)
from django.http import (
    HttpResponseRedirect,
    HttpResponse
)
from .models import (
    # We need to import our model to use it.
    Compute_resource_model,
    Profile_model,
    Operating_system_model,
    Create_host_model,
    Container_model
)
from main_app.modules import vm_manage as vm
from main_app.modules import kickstart, ssh_connect as ssh


# Create your views here.

def home(request):
    """
    We can pass the home.html as parameter to our render() function.

    :param request: .html page
    :return: home.html
    """
    return render(request, 'home.html')


def compute_resource(request):
    """
    We can pass the second parameter as infrastructure/compute_resource.html and third parameter as Dictionary to our.
    render() fuction
    :param request: .html page and Dictionary
    :return: compute_resource.html
    """
    form = Compute_resource_form()
    compute_resource_list = Compute_resource_model.objects.all()
    if not compute_resource_list:
        compute_resource_list = False
    # We create object of Compute_resource_model and fetch data and store in compute_resource_list variable
    return render(request, 'infrastructure/compute_resource.html',
                  {'title_name': 'Create New Compute Resource', 'form': form,
                   'compute_obj': compute_resource_list, 'message': False})


def post_data(request):
    form = Compute_resource_form(request.POST)
    compute_resource_list = Compute_resource_model.objects.all()
    if form.is_valid():
        compute = Compute_resource_model(
            name=form.cleaned_data["name"],
            ip_address=form.cleaned_data["ip_address"],
            root_password=form.cleaned_data["root_password"]
        )
        ssh_flag = ssh.make_connection(compute.ip_address, compute.root_password)
        if ssh_flag == True:

            try:
                compute.save()
                if make_connection(compute.ip_address, compute.name):
                    message = True
                else:
                    message = "Failed to add compute resource for docker"
            except IntegrityError as e:
                # message = "Name or Ip Address already exists"
                message = e

            form = Compute_resource_form()
            return render(request, 'infrastructure/compute_resource.html',
                          {'title_name': 'Create New Compute Resource', 'form': form,
                           'compute_obj': compute_resource_list, 'message': message})
        else:
            message = ssh_flag
            return render(request, 'infrastructure/compute_resource.html',
                          {'title_name': 'Create New Compute Resource', 'form': form,
                           'compute_obj': compute_resource_list, 'message': message})

def profile(request):
    form = Profile_form()
    profile_list = Profile_model.objects.all()
    if not profile_list:
        profile_list = False
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
    error = False
    os_name = Operating_system_model.objects.values_list("os_name", flat=True)
    if not os_name:
        error = "No Operating System Found"
    else:
        os_name = list(zip(os_name, os_name))
    profile_name = Profile_model.objects.values_list("profile_name", flat=True)
    if not profile_name:
        error = "No Profiles Found"
    else:
        profile_name = list(zip(profile_name, profile_name))
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    if not compute_name:
        error = "No Compute Resource Found"
    else:
        compute_name = list(zip(compute_name, compute_name))
    return render(request, 'host/create_host.html',
                  {'title_name': 'Create A New Host', 'form': form, 'os_name': os_name, 'compute_name': compute_name,
                   'profile_name': profile_name, 'error': error})


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

        profile_details = list(
            Profile_model.objects.filter(profile_name=create_host.select_vm_profile).values_list()[0])
        *not_imp1, ram, cpus, disk_size = profile_details

        compute_details = list(Compute_resource_model.objects.filter(name=create_host.select_compute).values_list()[0])
        *not_imp2, compute_ip, compute_passwd = compute_details

        os_details = list(Operating_system_model.objects.filter(os_name=create_host.vm_os).values_list()[0])
        *not_imp3, location_url = os_details

        root_passwd = form.data['password']
        kickstart_location = kickstart.kick_gen(root_passwd, location_url)
        vm.vm_create(compute_ip, create_host.vm_name, ram, cpus, disk_size, location_url, kickstart_location)
        create_host.save()
    return HttpResponseRedirect('/')


def new_container(request):
    form = newContainerform
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    compute_name = list(zip(compute_name, compute_name))
    return render(request, 'containers/new_container.html', \
                  {'title_name': "New Container", 'form': form, 'compute_name': compute_name})


def post_new_container(request):
    form = newContainerform(request.POST)
    if form.is_valid():
        new_cont = Container_model(
            select_compute=form.data['select_compute'],
            image_name=form.data['image_name'],
            tag_name=form.data['tag_name'],
            container_name=form.data['container_name'],
        )
        create_cont = "docker-machine ssh " + new_cont.select_compute + " docker container run -d -p " + \
                      form.data["host_port"] + ":" + form.data[
                          "cont_port"] + " --name " + new_cont.container_name + " " + \
                      new_cont.image_name + ":" + new_cont.tag_name
        print(create_cont)
        os.system(create_cont)
        # form.save()
    return HttpResponseRedirect('/')


def local_images(request):
    client = docker.from_env()
    images_list = {}
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    if not compute_name:
        compute_name = False
    else:
        print(compute_name)
        active_compute = compute_name[0]
        compute_name = list(zip(compute_name, compute_name))
        get_images = os.popen("docker-machine ssh " + active_compute + " docker images").readlines()
        for i in range(1, len(get_images)):
            images = get_images[i].split()
            images_list[images[2]] = [images[0], images[1], images[3] + " " + images[4] + " " + images[5], images[6]]
    return render(request, 'containers/local_images.html',
                  {'title_name': "Local Docker Images", 'images_list': images_list, 'compute_name': compute_name})


def post_local_images(request):
    form = Local_Images(request.POST)
    images_list = {}
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    compute_name = list(zip(compute_name, compute_name))
    cpt_name = form.data["select_compute"]
    get_images = os.popen("docker-machine ssh " + cpt_name + " docker images").readlines()
    for i in range(1, len(get_images)):
        images = get_images[i].split()
        images_list[images[2]] = [images[0], images[1], images[3] + " " + images[4] + " " + images[5], images[6]]
    return render(request, 'containers/local_images.html',
                  {'title_name': "Local Docker Images", 'images_list': images_list, \
                   'cpt_name': cpt_name, 'compute_name': compute_name})
