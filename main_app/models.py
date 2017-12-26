from django.db import models
from django import forms
# Create your models here.


#Model for Compute_resources
class Compute_resource_model(models.Model):
    name = models.CharField(max_length=10)
    ip_address = models.CharField(max_length=15)
    root_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


#Model for profile
class Profile_model(models.Model):
    newlist=compute_resource_model.objects.values_list("name",flat=True)
    newlist=list(zip(newlist,newlist))
    profile_name = models.CharField(max_length=10)
    ram = models.IntegerField()
    cpus = models.IntegerField()
    disk_size = models.IntegerField()
    select_compute = models.CharField(max_length=10,choices=newlist,default=None)

    def __str__(self):
        return self.profile_name


#Model for create host
class Create_host_model(models.Model):
    profile_names = profile_model.objects.values_list("profile_name",flat=True)
    profile_names = list(zip(profile_names,profile_names))
    vm_name = models.CharField(max_length=15)
    vm_os = models.CharField(max_length=15)
    select_vm_profile = models.CharField(max_length=10,choices=profile_names,default=None)

    def __str__(self):
        return self.vm_name


#Model for operating_system
class Operating_system_model(models.Model):
    os_name = models.CharField(max_length=15)
    os_location = models.CharField(max_length=100)

    def __str__(self):
        return self.os_name