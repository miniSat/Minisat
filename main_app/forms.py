from django import forms
from .models import *


class Compute_resource_form(forms.ModelForm):
    class Meta:
        model = Compute_resource_model
        fields = '__all__'



class Profile_form(forms.ModelForm):
    class Meta:
        model = Profile_model
        fields = '__all__'


class Create_host_form(forms.ModelForm):
    class Meta:
        model = Create_host_model
        fields = '__all__'

class Operating_system_form(forms.ModelForm):
    class Meta:
        model = Operating_system_model
        fields = '__all__'
