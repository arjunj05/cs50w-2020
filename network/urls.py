
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profiler>", views.profile, name="profile"),
    path('following', views.following, name="following"),
    path('update', views.update, name="update"),
    path('like', views.like, name="like"),
    path('loadLike', views.loadLike, name="loadLike")
]
