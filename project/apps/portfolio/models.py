from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='img/projects/', null=True, blank=True)
    url_deploy = models.URLField(null=True, blank=True)
    url_source = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title