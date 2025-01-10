from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from users.models import Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project
from .forms import ProjectForm

import json 

# Create your views here.
class IndexView(View):
    def get(self, request):
        context={}
        reviews = Review.objects.all().order_by("-id").filter(is_approved=True)
        context["reviews"] = reviews
        return render(request, 'portfolio/index.html', context)
    
class ContactView(View):
    def get(self, request):
        return render(request, 'portfolio/contact.html')
    
# Projects___________________
class ProjectListView(View):
    def get(self, request):
        return render(request, 'portfolio/project_list.html', {})
    

class LoadProjectListView(View):
    def get(self, request):
        consult = request.GET.get("consult", "")
        projects = Project.objects.all()

        if consult:
            projects = projects.filter(Q(title__icontains=consult) | Q(description__icontains=consult)).order_by("-id")
        paginator = Paginator(projects, 12) 
        page = request.GET.get('page')

        projects = paginator.get_page(page)
        context = {
            'object_list': projects,
            'consult': consult,
        }
        return render(request, 'portfolio/partials/project_list.html', context)
    

class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'portfolio/project_detail.html', {'project': project})


class ProjectCreateView(View, LoginRequiredMixin):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'portfolio/project_form.html', {'form': form})

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "projectListChanged": None,
                        "showMessage": "El proyecto se guardó correctamente."
                    })
                }
            )
        else:
            return render(request, 'portfolio/project_form.html', {'form': form})


class ProjectConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'portfolio/project_confirm_action.html', {'project': project})
    

class ProjectUpdateView(View, LoginRequiredMixin):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=project)
        return render(request, 'portfolio/project_form.html', {'form': form, 'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "projectListChanged": None,
                        "showMessage": "El proyecto se actualizó correctamente."
                    })
                }
            )
        else:
            return render(request, 'portfolio/project_form.html', {'form': form, 'project': project})
    
class ProjectDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "projectListChanged": None,
                    "showMessage":"El proyecto se eliminó correctamente."
                })
            }
        )
