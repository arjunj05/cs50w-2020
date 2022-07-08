from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:lID>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.category_list, name="categories"),
    path("watchlist/<int:lID>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist_list, name="watchlist"),
    path("endbid/<int:lID>", views.endbid, name="endbid"),
    path("past_listings", views.past_listings, name="past_listings"),
    path("past_listings/<int:lID>", views.pastList, name="past_listings"),
    path("comment/<int:lID>", views.comment, name="comment")
]
