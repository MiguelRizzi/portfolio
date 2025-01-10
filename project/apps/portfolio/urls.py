from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contacto/", views.ContactView.as_view(), name="contact"),


    path('portfolio/', views.ProjectListView.as_view(), name='project_list'),
    path('portfolio/listar/', views.LoadProjectListView.as_view(), name='load_project_list'),
    path('portfolio/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('portfolio/crear/', views.ProjectCreateView.as_view(), name='project_create'),
    path('portfolio/confirmar/actualizar/<int:pk>/', views.ProjectConfirmActionView.as_view(), name='project_confirm_update'),
    path('portfolio/actualizar/<int:pk>/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('portfolio/confirmar/eliminar/<int:pk>/', views.ProjectConfirmActionView.as_view(), name='project_confirm_delete'),
    path('portfolio/eliminar/<int:pk>/', views.ProjectDeleteView.as_view(), name='project_delete'),
]