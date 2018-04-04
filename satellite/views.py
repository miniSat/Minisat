from django.views.generic import TemplateView  # NOQA
import os
from django.shortcuts import render
from satellite.modules.docker_manage import (
    run_cont,
    make_connection,
    get_docker_images,
    start_cont,
    stop_cont,
    destroy_cont
)
from django.http import JsonResponse
import validators
# We'll use render to display our templates.

from .forms import (
    # We need to import our forms to use it.
    Compute_resource_form,
    Create_host_form,
    Profile_form,
    Operating_system_form,
    newContainerform,
    Product_form,
    View_form,
    Activation_form,
    Host_group_form,
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
    View_model,
    Activation_model,
    Host_group_model
)
from satellite.modules import vm_manage as vm
from satellite.modules import (
    kickstart,
    ssh_connect as ssh,
    dashboard_details as dash
)


# Create your views here.


def home(request):
    """
    Renders the home page.

    :param request: HttpRequest for loading the home page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    return render(request, 'home.html', {'title_name': "Dashboard"})


def get_virtual_mc(request):
    """
    Get all virtual machines running on all local imagess.

    :param request: HttpRequest to gather facts of virtual machines.

    :returns:       Dictionary of all virtual machines along with their facts.
    """
    compute_name = Compute_resource_model.objects.values_list()
    get_vms = dash.get_vms(compute_name)
    return JsonResponse(get_vms)


def get_running_containers(request):
    """
    Get all containers running on all compute resources.

    :param request: HttpRequest to gather facts of containers.

    :returns:       Dictionary of all containers along with their facts.
    """
    compute_name = Compute_resource_model.objects.values_list()
    get_containers = dash.running_containers(compute_name)
    return JsonResponse(get_containers)


def compute_resource(request):
    """
    Renders the compute resource page.

    :param request: HttpRequest for loading the compute resource page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = Compute_resource_form()
    compute_resource_list = Compute_resource_model.objects.all()
    if not compute_resource_list:
        compute_resource_list = False
    # We create object of Compute_resource_model and fetch data and store in
    return render(request, 'infrastructure/compute_resource.html',
                  {'title_name': 'Compute Resource',
                   'form': form,
                   'compute_obj': compute_resource_list,
                   'message': False
                   })


def post_data(request):
    """
    Receive post request from compute resource form.
    Validate the data.
    Check if the entered IP Address in alive.
    Add the system as compute for virtual machines and Docker containers.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to compute resource page along with other values needed by the template
    """
    form = Compute_resource_form(request.POST)
    compute_resource_list = Compute_resource_model.objects.all()
    message = ""
    if form.is_valid():
        compute = Compute_resource_model(
            name=form.cleaned_data["name"],
            ip_address=form.cleaned_data["ip_address"],
            root_password=form.cleaned_data["root_password"]
        )
        check_name = Compute_resource_model.objects.all().filter(name=compute.name).exists()
        check_ip = Compute_resource_model.objects.filter(ip_address=compute.ip_address).exists()
        if not check_name:
            if not check_ip:
                if vm.isOnline(compute.ip_address):
                    vm_result = ssh.make_connection(compute.ip_address, compute.root_password)
                    if vm_result == "True":
                        if make_connection(compute.ip_address, compute.name) == "True":
                            compute.save()
                            form = Compute_resource_form()
                            message = True
                        else:
                            message = "Could not add compute for Docker"
                    else:
                        message = vm_result
                else:
                    message = "System is unreachable"
            else:
                message = "IP address already exists"
        else:
            message = "Compute name already exists"
    else:
        message = "Invalid Field Data"

    return render(request, 'infrastructure/compute_resource.html',
                  {'title_name': 'Compute Resource',
                   'form': form,
                   'compute_obj': compute_resource_list,
                   'message': message})


def profile(request):
    """
    Renders the profile page.

    :param request: HttpRequest for loading the profile page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = Profile_form()
    profile_list = Profile_model.objects.all()
    if not profile_list:
        profile_list = False
    return render(request,
                  'infrastructure/profile.html',
                  {'title_name': 'Profile',
                   'form': form,
                   'message': False,
                   'profile_obj': profile_list})


def post_profile(request):
    """
    Receive post request from profile form.
    Validate the data.
    Save the user submitted values under a profile name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to profile page along with other values needed by the template.
    """
    form = Profile_form(request.POST)
    profile_list = Profile_model.objects.all()
    message = ""
    if form.is_valid():
        profile = Profile_model(
            profile_name=form.cleaned_data["profile_name"],
            ram=form.cleaned_data["ram"],
            cpus=form.cleaned_data["cpus"],
            disk_size=form.cleaned_data["disk_size"]
        )
        check_profile_name = Profile_model.objects.filter(profile_name=profile.profile_name).exists()
        if not check_profile_name:
            profile.save()
            form = Profile_form()
            message = True

        else:
            message = "Name Already exist"

    else:
        message = "Invalid Values"

    return render(request, 'infrastructure/profile.html',
                  {'title_name': 'Profile',
                   'form': form,
                   'profile_obj': profile_list,
                   'message': message})


def create_host(request):
    """
    Renders the create host page.
    Hide the form unless a single value of compute resource, profile and operating system exists.

    :param request: HttpRequest for loading the create host page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
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
    activation_list = Activation_model.objects.values_list("activation_name", flat=True)
    activation_list = set(activation_list)
    activation_name = list(zip(activation_list, activation_list))
    activation_name.insert(0, ("Choose Activation Key", "Choose Activation Key"))

    return render(request,
                  'host/create_host.html',
                  {'title_name': 'New Host',
                   'form': form,
                   'os_name': os_name,
                   'compute_name': compute_name,
                   'profile_name': profile_name,
                   'activation_name': activation_name,
                   'host_group': Host_group_model.objects.all(),
                   'error': error})


def operating_system(request):
    """
    Renders the operating system page.

    :param request: HttpRequest for loading the operating system page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = Operating_system_form()
    operating_system_list = Operating_system_model.objects.all()
    return render(request,
                  'host/operating_system.html',
                  {'title_name': 'Operating System',
                   'form': form,
                   'os_obj': operating_system_list,
                   'message': False})


def post_operating_system(request):
    """
    Receive post request from operating system form.
    Validate the data by accepting unique urls and names for operating system.
    Save the user submitted values under a operating system name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to profile page along with other values needed by the template.
    """
    form = Operating_system_form(request.POST)
    operating_system_list = Operating_system_model.objects.all()
    message = ""
    if form.is_valid():
        operating_sys = Operating_system_model(
            os_name=form.cleaned_data["os_name"],
            os_location=form.cleaned_data["os_location"]
        )
        check_os_name = Operating_system_model.objects.filter(os_name=operating_sys.os_name).exists()
        check_os_location = Operating_system_model.objects.filter(os_location=operating_sys.os_location).exists()
        val_url = validators.url(operating_sys.os_location)
        if val_url is True:
            if not check_os_name:
                if not check_os_location:
                    operating_sys.save()
                    message = True
                    form = Operating_system_form()
                else:
                    message = "Location already exist"
            else:
                message = "OS Name already exist"
        else:
            message = "Invalid URL"
    else:
        message = "Invalid Values"
    return render(request,
                  'host/operating_system.html',
                  {'title_name': 'Operating System',
                   'form': form,
                   'os_obj': operating_system_list,
                   'message': message})


def post_create_host(request):
    """
    Receive post request from create host form.
    Validate the data.
    Check whether activation key is added. If yes, pass the corresponding urls of repositories to kickstart file.
    Call the function vm_create. Pass necessary arguments to it to provision a virtual machine.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to home (dashboard) page along with other values needed by the template.
    """
    form = Create_host_form(request.POST)
    if form.is_valid():
        create_host = Create_host_model(
            vm_name=form.data['vm_name'],
            vm_os=form.data['vm_os'],
            select_vm_profile=form.data['select_vm_profile'],
            select_compute=form.data['select_compute'],
            activation_name=form.data['activation_name'],
            password=form.data['password']
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

        if create_host.activation_name == 'Choose Activation Key':
            repo = {}
        else:
            repo = vm.get_repo(create_host.activation_name)

        kickstart_location = kickstart.kick_gen(create_host.vm_name, create_host.password, location_url, repo)

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
    """
    Renders the new container page.

    :param request: HttpRequest for loading the new container page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
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
    """
    Receive post request from new container form.
    Validate the data.
    Check if the container is to be kept running in background.
    Call run_cont method, pass the parameters needed to run container along with the flag to decide whether the
    container is to be kept running in background or not.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to new container page along with other values needed by the template.
    """
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
        stat = ''
        try:
            if form.data["container_stat"] == "on":
                stat = "on"
        except:
            stat = ""

        run_cont(new_cont, stat)
    return HttpResponseRedirect('/')


def local_images(request):
    """
    Renders the local images page.

    :param request: HttpRequest for loading the local images page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
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
    """
    Receive get request from local images form.
    Get the compute name whose local Docker images have to be displayed.
    Call get_docker_images, pass the details of the compute resource selected by the user.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to local images page along with other values needed by the template
    """
    docker_images = {}
    com_name = request.GET.get('com_name', None)
    com_det = Compute_resource_model.objects.filter(name=com_name).values_list()
    docker_images = get_docker_images(com_det)
    return JsonResponse(docker_images)


def vm_info(request, cname, vm_id):
    """
    Renders the vm_info page.

    :param request: HttpRequest for loading the profile page.
    :param cname:   Compute resource name.
    :param vm_id:   UUID of a virtual machine running on a compute resource.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    compute = Compute_resource_model.objects.filter(name=cname).values_list()[0]
    compute_ip = compute[2]
    return render(request, 'VM_info.html', {'compute_ip': compute_ip, 'vm_id': vm_id})


def vm_start(request):
    """
    Turn on a virtual machine.

    :param request: HttpRequest from home page which brings vm_name and compute_name values.

    :returns:       Json object with current status of the virtual machine and a flag which shows whether the virutal
                    machine was successfully turned on or not.
    """
    data = {}
    vm_name = request.GET.get('vm_name', None)
    vm_compute_name = request.GET.get('compute_name', None)
    com_ip = list(Compute_resource_model.objects.filter(name=vm_compute_name).values_list(flat=True))[2]
    status = vm.virsh_start_vm(vm_name, com_ip)
    data['status'] = status
    data['vm_name'] = vm_name
    return JsonResponse(data)


def vm_pause(request):
    """
    Turn off a virtual machine.

    :param request: HttpRequest from home page which brings vm_name and compute_name values.

   :returns:        Json object with current status of the virtual machine and a flag which shows whether the virtual                      machine was successfully turned off or not.
    """
    data = {}
    vm_name = request.GET.get('vm_name', None)
    vm_compute_name = request.GET.get('compute_name', None)
    com_ip = list(Compute_resource_model.objects.filter(name=vm_compute_name).values_list(flat=True))[2]
    status = vm.virsh_pause_vm(vm_name, com_ip)
    data['status'] = status
    data['vm_name'] = vm_name
    return JsonResponse(data)


def vm_delete(request):
    """
    Delete a virtual machine.

    :param request: HttpRequest from home page which brings vm_name and compute_name values.

    :returns:       Json object with current status of the virtual machine and a flag which shows whether the virutal
                    virtual machine was successfully deleted or not.
    """
    data = {}
    vm_name = request.GET.get('vm_name', None)
    vm_compute_name = request.GET.get('compute_name', None)
    com_ip = list(Compute_resource_model.objects.filter(name=vm_compute_name).values_list(flat=True))[2]
    status = vm.virsh_delete_vm(vm_name, com_ip)
    data['status'] = status
    data['vm_name'] = vm_name
    return JsonResponse(data)


def start_container(request):
    """
    Start a container.

    :param request: HttpRequest from home page which brings container name and compute_name values.

    :returns:       Json object with current status of the container and a flag which shows whether the
                    container was successfully turned on or not.
    """
    cont_name = request.GET.get('cont_name', None)
    compute_name = request.GET.get('compute_name', None)
    container_status = start_cont(cont_name, compute_name)
    res = {'status': container_status, 'cont_name': cont_name}
    return JsonResponse(res)


def stop_container(request):
    """
    Stop a container.

    :param request: HttpRequest from home page which brings container name and compute_name values.

    :returns:       Json object with current status of the container and a flag which shows whether the
                    container was successfully turned off or not.
    """
    cont_name = request.GET.get('cont_name', None)
    compute_name = request.GET.get('compute_name', None)
    container_status = stop_cont(cont_name, compute_name)
    res = {'status': container_status, 'cont_name': cont_name}
    return JsonResponse(res)


def destroy_container(request):
    """
    Destroy a container.

    :param request: HttpRequest from home page which brings container name and compute_name values.

    :returns:       Json object with current status of the container and a flag which shows whether the
                    container was successfully destroyed or not.
    """
    cont_name = request.GET.get('cont_name', None)
    compute_name = request.GET.get('compute_name', None)
    container_status = destroy_cont(cont_name, compute_name)
    res = {'status': container_status, 'cont_name': cont_name}
    return JsonResponse(res)


def product(request):
    """
    Renders the product page.

    :param request: HttpRequest for loading the product page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = Product_form()
    product_list = Product_model.objects.all()
    return render(request,
                  'Content/product.html',
                  {'title_name': 'Product',
                   'form': form,
                   'product_obj': product_list,
                   'message': False})


def post_product(request):
    """
    Receive post request from product form.
    Validate the data.
    Save the user submitted values under a product name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to product page along with other values needed by the template.
    """
    form = Product_form(request.POST)
    product_list = Product_model.objects.all()
    message = ""
    if form.is_valid():
        product = Product_model(
            product_name=form.cleaned_data["product_name"],
            product_location=form.cleaned_data["product_location"]
        )
        check_product_name = Product_model.objects.filter(product_name=product.product_name).exists()
        val_url = validators.url(product.product_location)
        if val_url is True:
            if not check_product_name:
                product.save()
                form = Product_form
                message = True
            else:
                message = "Product name Already Exist"
        else:
            message = "Invalid URL"
    else:
        message = "Invalid Values"

    return render(request,
                  'Content/product.html',
                  {'title_name': 'Product',
                   'form': form,
                   'product_obj': product_list,
                   'message': message})


def delete(request):
    """
    Receive get request from compute resource, profile, product, operating system, view and hosts form.
    Validate the data.
    Delete the corresponding entry from database when received a request from the above forms.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to respective page who sent a request to delete a value.
    """
    if request.GET.get('ComputeDelete'):
        Compute_resource_model.objects.filter(name=request.GET.get('ComputeDelete')).delete()
        name = request.GET.get('ComputeDelete')
        cmd = "docker-machine rm " + name + " -f "
        os.system(cmd)
        return HttpResponseRedirect("compute_resource")

    elif request.GET.get('ProfileDelete'):
        Profile_model.objects.filter(id=request.GET.get('ProfileDelete')).delete()
        return HttpResponseRedirect("profile")

    elif request.GET.get('ProductDelete'):
        product_name = Product_model.objects.filter(id=request.GET.get('ProductDelete')).values_list('product_name', flat=True)[0]
        Product_model.objects.filter(id=request.GET.get('ProductDelete')).delete()
        View_model.objects.all().filter(select_product=product_name).delete()
        return HttpResponseRedirect("product")

    elif request.GET.get('OSDelete'):
        Operating_system_model.objects.filter(id=request.GET.get('OSDelete')).delete()
        return HttpResponseRedirect("operating_system")

    elif request.GET.get('ViewDelete'):
        view_name = request.GET.get('ViewDelete')
        View_model.objects.filter(view_name=view_name).delete()
        Activation_model.objects.filter(select_view=view_name).delete()
        return HttpResponseRedirect('view')

    elif request.GET.get('HostGroupDelete'):
        host_group_name = request.GET.get('HostGroupDelete')
        Host_group_model.objects.filter(host_group_name=host_group_name).delete()
        return HttpResponseRedirect('host_group')

    return HttpResponseRedirect("/")


def get_updated_views():
    """
    Create a dictionary with view name as key and the products under that key as value.
    Display this dictionary in view existing tab of content view.

    :param request: None

    :returns:       Dictionary with all existing views along with their respective product urls.
    """
    view_dict = {}
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
    return view_dict


def get_updated_activations():
    """
    Create a dictionary with activation name as key and the views under that key as value.
    Display this dictionary in view existing tab of activation key view.

    :param request: None

    :returns:       Dictionary with all existing views with their views and product urls.
    """
    act_dict = {}
    acts = Activation_model.objects.all().values_list('activation_name', flat=True).distinct()
    for act in acts:
        viewList = Activation_model.objects.all().filter(activation_name=act).values_list()
        tmp = {}
        for each in viewList:
            productList = View_model.objects.all().filter(view_name=each[2]).values_list()
            li = {}
            for product in productList:
                products = Product_model.objects.all().filter(product_name=product[2]).values_list()
                for one in products:
                    li[one[1]] = one[2]
            tmp[each[2]] = li
        act_dict[act] = tmp
    return act_dict


def content_view(request):
    """
    Renders the content view page.

    :param request: HttpRequest for loading the content view page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = View_form()
    product_list = Product_model.objects.all()
    return render(request, 'Content/content_view.html',
                  {'title_name': "Content View",
                   'form': form,
                   'products': product_list,
                   'message': False,
                   'view_dict': get_updated_views()})


def post_content_view(request):
    """
    Receive post request from content view form.
    Validate the data.
    Save the user submitted values under a view name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to content view page along with other values needed by the template.
    """
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
    return render(request, 'Content/content_view.html',
                  {'title_name': "Content View", 'form': form, 'products': product_list, 'message': message,
                   'view_dict': get_updated_views()})


def activation_view(request):
    """
    Renders the activation key page.

    :param request: HttpRequest for loading the activation key page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    form = Activation_form()
    return render(request, 'Content/activation_key.html',
                  {'title_name': 'Activation Key', 'form': form, 'view_dict': get_updated_views(), 'message': False,
                   'act_dict': get_updated_activations(), 'tmp_var': ''})


def post_activation_view(request):
    """
    Receive post request from acitvation key form.
    Validate the data.
    Save the user submitted values under a view name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to activation page along with other values needed by the template.
    """
    form = Activation_form(request.POST)
    activation_name = request.POST.get('activation_name')
    view_list = request.POST.getlist('views[]')
    message = ''
    if not view_list:
        message = 'Select atleast one view'
    else:
        if not Activation_model.objects.all().filter(activation_name=activation_name).exists():
            for view in view_list:
                data = Activation_model(
                    activation_name=activation_name,
                    select_view=view
                )
                data.save()
                message = True
        else:
            message = 'Activation name already exists'
    return render(request, 'Content/activation_key.html',
                  {'title_name': 'Activation Key', 'form': form, 'message': message, 'view_dict': get_updated_views(),
                   'act_dict': get_updated_activations()})


def host_group_view(request):
    """
    Renders the host group page.

    :param request: HttpRequest for loading the host group page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    select_compute = Compute_resource_model.objects.values_list("name", flat=True)
    select_profile = Profile_model.objects.values_list("profile_name", flat=True)
    select_os = Operating_system_model.objects.values_list("os_name", flat=True)
    select_activation = Activation_model.objects.values_list("activation_name", flat=True).distinct()
    form = Host_group_form()
    return render(request, 'host_group/host_group.html', {
        'form': form,
        'title_name': "Host Group",
        'select_compute': select_compute,
        'select_profile': select_profile,
        'select_os': select_os,
        'select_activation': select_activation,
        'message': False,
        'host_group_dict': Host_group_model.objects.all()
    })


def post_host_group(request):
    """
    Receive post request from host group form.
    Validate the data.
    Save the user submitted values under a view name in database.

    :param request: HttpRequest with user submitted values in the form.

    :returns:       HttpResponse to redirect to host group page along with other values needed by the template.
    """
    form = Host_group_form(request.POST)
    select_compute = Compute_resource_model.objects.values_list("name", flat=True)
    select_profile = Profile_model.objects.values_list("profile_name", flat=True)
    select_os = Operating_system_model.objects.values_list("os_name", flat=True)
    select_activation = Activation_model.objects.values_list("activation_name", flat=True).distinct()
    message = ""
    if form.is_valid():
        if not Host_group_model.objects.all().filter(host_group_name=form.cleaned_data['host_group_name']).exists():
            form = Host_group_model(
                host_group_name=form.cleaned_data['host_group_name'],
                select_compute=form.cleaned_data['select_compute'],
                select_profile=form.cleaned_data['select_profile'],
                select_os=form.cleaned_data['select_os'],
                select_activation=form.cleaned_data['select_activation'],
            )
            form.save()
            message = True
            form = Host_group_form()
        else:
            message = "Host Group Already Exists"
    else:
        message = "Invalid Fields"

    return render(request, 'host_group/host_group.html', {
        'title_name': "Host Group",
        'select_compute': select_compute,
        'select_profile': select_profile,
        'select_os': select_os,
        'select_activation': select_activation,
        'form': form,
        'message': message,
        'host_group_dict': Host_group_model.objects.all(),
    })


def host_group_data(request):
    """
    Receive a post request with host group name.

    :param request: HttpRequest for with host group name.

    :returns:       Json object with host group name, compute, profile, operating system, activation key.
    """
    host_group = request.GET.get("host_group")
    host_data = list(Host_group_model.objects.all().filter(host_group_name=host_group).values_list(flat=True))
    data = {
        'host_group_name': host_data[1],
        'compute': host_data[2],
        'profile': host_data[3],
        'operating_system': host_data[4],
        'activation_key': host_data[5]
    }
    return JsonResponse(data)


def get_vm_packages(request, compute_ip, compute_name, vm_ip, vm_name):
    """
    Get the packages installed in the virtual machine.
    Called from vm_info page.

    :param request:         HttpRequest to fetch packages.
    :param compute_ip:      IP address of compute resource, where the virtual machine is running.
    :param compute_name:    Name of compute resource, where the virtual machine is running.
    :param vm_ip:           IP address of virtual machine, whose packages need to fetched.
    :param vm_name:         Name of virtual machine, whose packages need to fetched.

    :returns:               Json object with list of all the packages installed in the virtual machine.
    """
    data = {}
    compute_ip = compute_ip.replace('-', '.')
    vm_ip = vm_ip.replace('-', '.')
    root_passwd = Create_host_model.objects.filter(select_compute=compute_name, vm_name=vm_name).values_list()[0][6]
    data['packages'] = vm.get_packages(compute_ip, vm_ip, root_passwd)
    return JsonResponse(data)


def get_vm_facts(request, compute_ip, vm_id):
    """
    Get the details of a the virtual machine.
    Called from vm_info page.

    :param request:         HttpRequest to fetch facts.
    :param compute_ip:      IP address of compute resource, where the virtual machine is running.
    :param vm_id:           UUID of the targeted virtual machine.

    :returns:               Json object with list of all the details about the virtual machine.
    """
    compute_ip = compute_ip.replace('-', '.')
    compute_name = Compute_resource_model.objects.filter(ip_address=compute_ip).values_list()[0][1]
    details = vm.vm_details(compute_name, compute_ip, vm_id)
    OS = Create_host_model.objects.filter(select_compute=compute_name, vm_name=details["Name"]).values_list()[0][2]
    details["Operating System"] = OS
    return JsonResponse(details)


def get_added_repo(request, compute_ip, vm_ip, vm_name):
    """
    Get the details of all the repositories added in the virtual machine.
    Called from vm_info page.

    :param request:         HttpRequest to fetch packages.
    :param compute_ip:      IP address of compute resource, where the virtual machine is running.
    :param vm_ip:           IP address of the virtual machine whose repositories need to found.
    :param vm_name:         Name of virtual machine, whose repositories need to fetched.

    :returns:               Json object with list of all the details about the repositories in virtual machine.
    """
    compute_ip = compute_ip.replace('-', '.')
    vm_ip = vm_ip.replace('-', '.')
    result = vm.get_vm_repo(compute_ip, vm_ip, vm_name)
    return JsonResponse(result)


def get_vm_status(request, compute_ip, vm_name, vm_ip):
    """
    Get the current state of a virtual machine.

    :param request:         HttpRequest to get status.
    :param compute_ip:      IP address of compute resource, where the virtual machine is running.
    :param vm_ip:           IP address of the virtual machine whose state need to found.
    :param vm_name:         Name of virtual machine, whose state need to fetched.

    :returns:               Json object with list of all the details about the state of the virtual machine.
    """
    result = vm.vm_status(compute_ip, vm_name, vm_ip)
    return JsonResponse(result)


def change_repo_state(request, compute_ip, vm_ip, repo_id, repo_flag, vm_name):
    """
    Toggle the repository between enabled to disabled.

    :param request:         HttpRequest to change repo state.
    :param compute_ip:      IP address of compute resource, where the virtual machine is running.
    :param vm_ip:           IP address of the virtual machine whose repo state needs to found.
    :param repo_id:         Repository id of which is to be toggled.
    :param repo_flag:       Decide whether it is to be enabled or disabled.
    :param vm_name:         Name of virtual machine, whose state need to fetched.

    :returns:               Json object with changed state of a particular repository from the virtual machine.
    """
    get_repo_state = vm.change_repo(compute_ip, vm_ip, repo_id, repo_flag, vm_name)
    return JsonResponse({'flag': get_repo_state})


def error_404(request):
    """
    Renders the error page.

    :param request: HttpRequest for loading the error page.

    :returns:       HttpResponse with template name and the parameters needed by the template.
    """
    return render(request, 'error/error404.html')
