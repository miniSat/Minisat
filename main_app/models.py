from django.db import models

# Create your models here.

class compute_resource(models.Model):
    name = models.CharField(max_length=10)
    ip_address = models.CharField(max_length=15)
    root_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name