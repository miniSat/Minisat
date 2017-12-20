from django.db import models
from django import forms
# Create your models here.


#Model for Compute_resources
class compute_resource_model(models.Model):
    name = models.CharField(max_length=10)
    ip_address = models.CharField(max_length=15)
    root_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

#Model for profile
class profile_model(models.Model):
    newlist=compute_resource_model.objects.values_list("name",flat=True)
    newlist=list(zip(newlist,newlist))
    profile_name = models.CharField(max_length=10)
    ram = models.IntegerField()
    cpus = models.IntegerField()
    disk_size = models.IntegerField()
    select_compute = models.CharField(max_length=10,choices=newlist,default=None)

    def __str__(self):
        return self.profile_name


