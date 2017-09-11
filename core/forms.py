from django import forms
from django.forms import ModelForm
from .models import Transform

class TransformForm(ModelForm):
    class Meta:
        model = Transform
        fields = '__all__'
