from django.urls import path
from . import views


urlpatterns = [
    
    path("", views.index, name="index"),
    path("<str:name>", views.page, name = "page"),
    path("", views.page, name = "searching"),
]