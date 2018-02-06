from django.views.generic import TemplateView  # NOQA
import docker
import os
from django.shortcuts import render
from main_app.modules.docker_manage import make_connection, get_docker_images, start_cont, stop_cont
from django.http import JsonResponse
# We'll use render to display our templates.

from .forms import (
    # We need to import our forms to use it.
    Compute_resource_form,
    Create_host_form,
    Profile_form,
    Operating_system_form,
    newContainerform,
    Product_form,
    View_form
)
from django.http import (
    HttpResponseRedirect
)
from .models import (
    # We need to import our model to use it.
    Compute_resource_model,
    Profile_model,
    Operating_system_model,
    Create_host_model,
    Container_model,
    Product_model,
    View_model)
from main_app.modules import vm_manage as vm
from main_app.modules import (
    kickstart,
    ssh_connect as ssh,
    dashboard_details as dash
)


# Create your views here.


def home(request):
    """
    We can pass the home.html as parameter to our render() function.

    :param request: .html page
    :return: home.html
    """
    return render(request, 'home.html')


def get_virtual_mc(request):
    compute_name = Compute_resource_model.objects.values_list()
    get_vms = dash.get_vms(compute_name)
    return JsonResponse(get_vms)


def get_running_containers(request):
    compute_name = Compute_resource_model.objects.values_list()
    get_containers = dash.running_containers(compute_name)
    return JsonResponse(get_containers)


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
    # We create object of Compute_resource_model and fetch data and store in
    # compute_resource_list variable
    return render(request, 'infrastructure/compute_resource.html',
                  {'title_name': 'Create New Compute Resource', 'form': form,
                   'compute_obj': compute_resource_list})


def post_data(request):
    message = {}
    if (request.is_ajax() and request.method == 'POST'):
        name = request.POST["name"]
        ip_address = request.POST["ip_address"]
        root_password = request.POST["root_password"]
        check_name = Compute_resource_model.objects.all().filter(name=name).exists()
        check_ip = Compute_resource_model.objects.filter(ip_address=ip_address).exists()
        if not check_name:
            if not check_ip:
                if vm.isOnline(ip_address):
                    vm_result = ssh.make_connection(ip_address, root_password)
                    if vm_result == "True":
                        if make_connection(ip_address, name) == "True":
                            compute_obj = Compute_resource_model(
                                name=name,
                                ip_address=ip_address,
                                root_password=root_password
                            )
                            compute_obj.save()
                        else:
                            message['docker-status'] = "Could not add compute for Docker"
                    else:
                        message['vm-status'] = vm_result
                else:
                    message["status"] = "System is unreachable"
            else:
                message["status"] = "IP address already exists"
        else:
            message["status"] = "Compute name already exists"
    print(message)
    return JsonResponse(message)


def profile(request):
    form = Profile_form()
    profile_list = Profile_model.objects.all()
    if not profile_list:
        profile_list = False
    return render(request,
                  'infrastructure/profile.html',
                  {'title_name': 'Profile',
                   'form': form,
                   'profile_obj': profile_list})


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
    compute_name = Compute_resource_model.objects.values_list(
        "name", flat=True)
    if not compute_name:
        error = "No Compute Resource Found"
    else:
        compute_name = list(zip(compute_name, compute_name))
    return render(request,
                  'host/create_host.html',
                  {'title_name': 'Create A New Host',
                   'form': form,
                   'os_name': os_name,
                   'compute_name': compute_name,
                   'profile_name': profile_name,
                   'error': error})


def operating_system(request):
    form = Operating_system_form()
    operating_system_list = Operating_system_model.objects.all()
    return render(request,
                  'host/operating_system.html',
                  {'title_name': 'Add Operating System',
                   'form': form,
                   'os_obj': operating_system_list})


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

        profile_details = list(Profile_model.objects.filter(
            profile_name=create_host.select_vm_profile).values_list()[0])
        *not_imp1, ram, cpus, disk_size = profile_details

        compute_details = list(
            Compute_resource_model.objects.filter(
                name=create_host.select_compute).values_list()[0])
        *not_imp2, compute_ip, compute_passwd = compute_details

        os_details = list(
            Operating_system_model.objects.filter(
                os_name=create_host.vm_os).values_list()[0])
        *not_imp3, location_url = os_details

        root_passwd = form.data['password']
        kickstart_location = kickstart.kick_gen(root_passwd, location_url)
        vm.vm_create(
            compute_ip,
            create_host.vm_name,
            ram,
            cpus,
            disk_size,
            location_url,
            kickstart_location)
        create_host.save()
    return HttpResponseRedirect('/')


def new_container(request):
    form = newContainerform
    compute_name = Compute_resource_model.objects.values_list(
        "name", flat=True)
    compute_name = list(zip(compute_name, compute_name))
    return render(request,
                  'containers/new_container.html',
                  {'title_name': "New Container",
                   'form': form,
                   'compute_name': compute_name})


def post_new_container(request):
    form = newContainerform(request.POST)

    if form.is_valid():
        new_cont = Container_model(
            select_compute=form.data['select_compute'],
            image_name=form.data['image_name'],
            tag_name=form.data['tag_name'],
            container_name=form.data['container_name'],
            host_port=form.data["host_port"],
            cont_port=form.data["cont_port"]
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
    client = docker.from_env()  # NOQA
    compute_name = Compute_resource_model.objects.values_list("name", flat=True)
    if not compute_name:
        compute_name = False
    else:
        compute_name = list(zip(compute_name, compute_name))
    return render(request,
                  'containers/local_images.html',
                  {'title_name': "Local Docker Images",
                   'compute_name': compute_name})


def post_local_images(request):
    docker_images = {}
    com_name = request.GET.get('com_name', None)
    com_det = Compute_resource_model.objects.filter(name=com_name).values_list()
    docker_images = get_docker_images(com_det)
    print(docker_images)
    return JsonResponse(docker_images)


def vm_info(request, cname, vm_id):
        compute = Compute_resource_model.objects.filter(name=cname).values_list()[0]
        compute_ip = compute[2]
        details = vm.vm_details(compute_ip, vm_id)
        OS = Create_host_model.objects.filter(select_compute=cname, vm_name=details["Name"]).values_list()[0][2]
        details["Operating System"] = OS
        packages = vm.get_packages(compute_ip, details["IP Address"])
        return render(request, 'VM_info.html', {"details": details, "packages": packages})


def vm_start(request):
    data = {}
    vm_name = request.GET.get('vm_name', None)
    vm_compute_name = request.GET.get('compute_name', None)
    com_ip = list(Compute_resource_model.objects.filter(name=vm_compute_name).values_list(flat=True))[2]
    status = vm.virsh_start_vm(vm_name, com_ip)
    data['status'] = status
    data['vm_name'] = vm_name
    return JsonResponse(data)


def vm_pause(request):
    data = {}
    vm_name = request.GET.get('vm_name', None)
    vm_compute_name = request.GET.get('compute_name', None)
    com_ip = list(Compute_resource_model.objects.filter(name=vm_compute_name).values_list(flat=True))[2]
    status = vm.virsh_pause_vm(vm_name, com_ip)
    data['status'] = status
    data['vm_name'] = vm_name
    return JsonResponse(data)


def start_container(request):
    cont_name = request.GET.get('cont_name', None)
    compute_name = request.GET.get('compute_name', None)
    container_status = start_cont(cont_name, compute_name)
    res = {'status': container_status, 'cont_name': cont_name}
    return JsonResponse(res)


def stop_container(request):
    cont_name = request.GET.get('cont_name', None)
    compute_name = request.GET.get('compute_name', None)
    container_status = stop_cont(cont_name, compute_name)
    res = {'status': container_status, 'cont_name': cont_name}
    return JsonResponse(res)


def product(request):
    form = Product_form()
    product_list = Product_model.objects.all()
    return render(request,
                  'Content/product.html',
                  {'title_name': 'Product',
                   'form': form,
                   'product_obj': product_list})


def post_product(request):
    form = Product_form(request.POST)
    if form.is_valid():
        product = Product_model(
            product_name=form.cleaned_data["product_name"],
            product_location=form.cleaned_data["product_location"]
        )
        product.save()
    return HttpResponseRedirect('/')


def delete(request):
    if(request.GET.get('ComputeDelete')):
        Compute_resource_model.objects.filter(id=request.GET.get('ComputeDelete')).delete()
    if(request.GET.get('ProfileDelete')):
        Profile_model.objects.filter(id=request.GET.get('ProfileDelete')).delete()
    if(request.GET.get('ProductDelete')):
        Product_model.objects.filter(id=request.GET.get('ProductDelete')).delete()
    if(request.GET.get('OSDelete')):
        Operating_system_model.objects.filter(id=request.GET.get('OSDelete')).delete()
    return HttpResponseRedirect("/")


def content_view(request):
    form = View_form()
    view_dict = {}
    product_list = Product_model.objects.all()
    viewList = View_model.objects.all().values_list('view_name', flat=True).distinct()
    for each in viewList:
        var = View_model.objects.all().filter(view_name=each).values()
        tmp = []
        for one in var:
            product = one['select_product']
            product_url = Product_model.objects.all().filter(product_name=product).values()[0]['product_location']
            myTup = (product, product_url)
            tmp.append(myTup)
        view_dict[each] = tmp
    return render(request, 'Content/content_view.html', {'title_name': "Content View", 'form': form, 'products': product_list, 'message': False, 'view_dict': view_dict})


def post_content_view(request):
    form = View_form(request.POST)
    view_name = request.POST.get('view_name')
    product_list = Product_model.objects.all()
    message = ""
    product_names = request.POST.getlist('products[]')
    if not product_names:
        message = "Select atleast one product"
    else:
        if not View_model.objects.all().filter(view_name=view_name).exists():
            for product in product_names:
                data = View_model(
                    view_name=view_name,
                    select_product=product
                )
                data.save()
                message = True
        else:
            message = "Name already exists"
    return render(request, 'Content/content_view.html', {'title_name': "Content View", 'form': form, 'products': product_list, 'message': message})
