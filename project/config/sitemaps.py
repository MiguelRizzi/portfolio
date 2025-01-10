from django.contrib.sitemaps import Sitemap
from blog.models import Post

class NobodiesSitemap(Sitemap):
    pass
from django.urls import reverse
    
class HomeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0
    def items(self):
        return ['portfolio:index']
    def location(self, item):
        return reverse(item)
    

class ContactSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.4
    def items(self):
        return ['portfolio:contact']
    def location(self, item):
        return reverse(item)
    
class BlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    def items(self):
        return ['blog:index']
    def location(self, item):
        return reverse(item)


    
class PostsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.last_modified