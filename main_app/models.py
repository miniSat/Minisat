from django.db import models
from django import forms
# Create your models here.


# Model for Compute_resources
class Compute_resource_model(models.Model):
    name = models.CharField(max_length=10)
    ip_address = models.CharField("IP Address", max_length=15)
    root_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Model for profile
class Profile_model(models.Model):
    newlist = Compute_resource_model.objects.values_list("name", flat=True)
    newlist = list(zip(newlist, newlist))
    profile_name = models.CharField(max_length=10)
    ram = models.IntegerField("RAM(GiB)")
    cpus = models.IntegerField("CPUs")
    disk_size = models.IntegerField("Disk Size(GiB)")
    select_compute = models.CharField(max_length=10, choices=newlist, default=None)

    def __str__(self):
        return self.profile_name


# Model for operating_system
class Operating_system_model(models.Model):
    os_name = models.CharField("OS Name", max_length=15)
    os_location = models.CharField("OS Location", max_length=100)

    def __str__(self):
        return self.os_name


# Model for create host
class Create_host_model(models.Model):
    profile_names = Profile_model.objects.values_list("profile_name", flat=True)
    profile_names = list(zip(profile_names, profile_names))
    os_name = Operating_system_model.objects.values_list("os_name", flat=True)
    os_name = list(zip(os_name,os_name))
    vm_name = models.CharField(max_length=15)
    vm_os = models.CharField(max_length=15,choices=os_name, default=None)
    select_vm_profile = models.CharField(max_length=10, choices=profile_names, default=None)

    def __str__(self):
        return self.vm_name


# Model for new container
class Container_model(models.Model):
    newlist = Compute_resource_model.objects.values_list("name", flat=True)
    newlist = list(zip(newlist, newlist))
    select_compute_resource = models.CharField("Select Compute Resource",max_length=15,choices=newlist,default=None)
    image_name = models.CharField("Image Name", max_length=20)
    tag_name = models.CharField("Tag", max_length=20)
    container_name = models.CharField("Container Name", max_length=20)
    command = models.CharField("Command",max_length=15)
    entry_point = models.CharField("Entry Point", max_length=15)



