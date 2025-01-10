from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        labels = {
            "title": "Título",
            "description": "Descripción",
            "image": "Fotografía",
            "url_deploy": "URL del proyecto",
            "url_source": "URL del código fuente",
        }
