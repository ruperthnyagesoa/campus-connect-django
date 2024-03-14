
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path("unfollow/<int:id>/", views.unfollow, name="unfollow"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("following", views.following, name="following"),
    path("like/<int:id>/", views.like, name="like"),
    path("class", views.class_ai, name="class_ai"),
]
