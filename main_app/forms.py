from django import forms
from .models import compute_resource,profile

class compute_resource_form(forms.ModelForm):
    class Meta:
        model = compute_resource
        fields = ['name', 'ip_address', 'root_password']


class profile_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['profile_name','ram','cpus','disk_size']