from django import forms
from .models import compute_resource

class compute_resource_form(forms.ModelForm):
    class Meta:
        model = compute_resource
        fields = ['name', 'ip_address', 'root_password']