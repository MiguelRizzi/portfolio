from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("listar/", views.LoadPostListView.as_view(), name="load_post_list"),
    path("crear/", views.PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("actualizar/<slug:slug>/", views.PostUpdateView.as_view(), name="post_update"),
    path("confirmar-eliminar/<slug:slug>/", views.PostConfirmActionView.as_view(), name="post_confirm_delete"),
    path("eliminar/<slug:slug>/", views.PostDeleteView.as_view(), name="post_delete"),
]