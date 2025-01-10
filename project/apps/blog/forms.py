from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'file', 'body','description', 'status']
        labels = {
            'title': 'Titulo',
            'file': 'Archivo',
            'body': 'Contenido',
            "description": "Descripción",
            'status': 'Estado',
        }
   