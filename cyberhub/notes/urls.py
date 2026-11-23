from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.folder_list, name="list"),
    path("folders/new/", views.folder_create, name="folder_create"),
    path("folders/<int:pk>/", views.folder_detail, name="folder_detail"),
    path("folders/<int:parent_id>/new/", views.folder_create, name="subfolder_create"),
    path("folders/<int:pk>/rename/", views.folder_rename, name="folder_rename"),
    path("folders/<int:pk>/delete/", views.folder_delete, name="folder_delete"),
]
