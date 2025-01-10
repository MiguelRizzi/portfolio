import json

from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import PostForm
from .models import Post



class IndexView(View):
    def get(self, request):
        featured_posts = Post.objects.filter(status="featured").order_by("-id")
        context={
            "featured_posts": featured_posts,
            "site_name": "Laura Chalú Blog",
            "description": ""

        }
        return render(request, 'blog/index.html', context)
    

class LoadPostListView(View):
    def get(self, request):
        consult = request.GET.get("consult", "")
        posts = Post.objects.filter(Q(title__icontains=consult) | Q(body__icontains=consult)).order_by("-id")
        if not request.user.is_authenticated:
            posts = posts.exclude(status="draft")
            
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        
        posts = paginator.get_page(page)
   
        context = {
            'object_list': posts,
            'consult': consult,
        }
        return render(request, 'blog/partials/post_list.html', context)
        

class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context= {
            "post": post,
            "site_name": post.title,
            "description": post.description
        }
        return render(request, 'blog/post_detail.html', context)


class PostCreateView(View, LoginRequiredMixin):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post= Post.objects.create(
            user = self.request.user,
            title = form.cleaned_data['title'],
            file = form.cleaned_data['file'],
            body = form.cleaned_data["body"],
            description = form.cleaned_data["description"],
            status = form.cleaned_data["status"],

            )

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": "El artículo se creó correctamente."
                    })
                }
            )
        else:
            return render(request, 'blog/post_form.html', {'form': form})


class PostConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'blog/post_confirm_action.html', {'post': post})
    

class PostUpdateView(View, LoginRequiredMixin):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form, 'post': post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": "El articulo se actualizó correctamente."
                    })
                }
            )
        else:
            return render(request, 'blog/post_form.html', {'form': form, 'post': post})
    

class PostDeleteView(View, LoginRequiredMixin):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "postListChanged": None,
                    "showMessage": "El articulo se eliminó correctamente."
                })
            }
        )