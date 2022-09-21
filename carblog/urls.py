from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    #path("page", views.page, name="page"),
    path("page/<str:title>", views.page, name="page"),
    path("create", views.create, name="create"),
    path("request", views.request, name="request"),
    path("filter", views.filter, name="filter"),
    path("brands",views.brands, name="brands")
]