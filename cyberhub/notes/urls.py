from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.folder_list, name="list"),
    path("history/back/", views.history_back, name="history_back"),
    path("history/forward/", views.history_forward, name="history_forward"),
    path("folders/new/", views.folder_create, name="folder_create"),
    path("folders/<int:pk>/", views.folder_detail, name="folder_detail"),
    path("folders/<int:parent_id>/new/", views.folder_create, name="subfolder_create"),
    path("folders/<int:pk>/rename/", views.folder_rename, name="folder_rename"),
    path("folders/<int:pk>/delete/", views.folder_delete, name="folder_delete"),
    path("folders/<int:folder_id>/notes/new/", views.note_create, name="note_create"),
    path("notes/preview/", views.note_preview, name="note_preview"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/edit/", views.note_edit, name="note_edit"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),
]
