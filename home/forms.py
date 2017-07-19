from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Upload

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('document',)
