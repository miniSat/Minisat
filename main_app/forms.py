from django import forms
from django.forms import Textarea, TextInput
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
