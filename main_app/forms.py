from django import forms
from django.forms import Textarea, TextInput
from .models import *


class Compute_resource_form(forms.Form):
    name = forms.CharField(label="Name", max_length=10)
    ip_address = forms.CharField(label="IP Address", max_length=15)
    root_password = forms.CharField(label="Root Password", max_length=20)


class Profile_form(forms.Form):
    profile_name = forms.CharField(label="Profile Name", max_length=10)
    ram = forms.IntegerField(label="RAM(MB)")
    cpus = forms.IntegerField(label="CPUs")
    disk_size = forms.IntegerField(label="Disk Size(GB)")


class Create_host_form(forms.Form):
    vm_name = forms.CharField(label="VM Name")
    vm_os = forms.CharField(label="VM OS")
    select_vm_profile = forms.CharField(label="VM Profile")
    select_compute = forms.CharField(label="Compute")

class Operating_system_form(forms.Form):
    os_name = forms.CharField(label="Name", max_length=15)
    os_location = forms.CharField(label="Location", max_length=100)


class newContainerform(forms.ModelForm):
    class Meta:
        model = Container_model
        fields = '__all__'


class Local_image_form(forms.ModelForm):
    class Meta:
        model = Local_image_model
        widgets = {
            'dockerfile': Textarea(attrs={'cols': 99, 'rows': 18, 'resize': 'vertical'})
        }
        fields = '__all__'
