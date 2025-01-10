from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
"""
from .sitemaps import HomeSitemap, BlogSitemap, PostsSitemap  

sitemaps = {
    'home': HomeSitemap,
    'blog': BlogSitemap,
    'posts': PostsSitemap,
}
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("portfolio.urls", "portfolio"))),
    path("", include(("users.urls", "users"))),
    path("blog/", include(("blog.urls", "blog"))),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Valido en entorno de desarrollo: DEBUG= True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()