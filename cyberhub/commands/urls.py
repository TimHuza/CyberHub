from django.urls import path

from . import views

app_name = "commands"

urlpatterns = [
    path("", views.library, name="library"),
    path("<int:pk>/", views.tab_detail, name="tab_detail"),
]
