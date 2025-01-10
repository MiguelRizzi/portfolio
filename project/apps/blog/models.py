from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils import validate_img_extension, validate_video_extension
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('featured', 'Destacado'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=160, null=True, blank=True)
    body = models.TextField()
    file = models.FileField(upload_to='uploads/blog/')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)  
    last_modified = models.DateTimeField(auto_now=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField(max_length=255, unique=True)


    def clean(self) -> None:
        if self.file:
            if not validate_img_extension(self.file) and not validate_video_extension(self.file):
                raise ValidationError("El archivo debe ser una imagen o un video.")

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        if Post.objects.exclude(id=self.id).filter(slug=slug).exists():
            self.slug = f"{slug}-{self.id}"
        else:
            self.slug = slug
        super().save(*args, **kwargs)
        return 

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.slug)])