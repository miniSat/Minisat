from django.db import models

# Create your models here.

#Model for Compute_resources
class compute_resource(models.Model):
    name = models.CharField(max_length=10)
    ip_address = models.CharField(max_length=15)
    root_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

#Model for profile
class profile(models.Model):
    profile_name = models.CharField(max_length=10)
    ram = models.IntegerField()
    cpus = models.IntegerField()
    disk_size = models.IntegerField()

    def __str__(self):
        return self.profile_name


