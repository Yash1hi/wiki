from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createPage", views.createPage, name="createPage"),
    path("createAPI", views.createAPI, name="createAPI"),
    path("<str:title>", views.title, name="title")
]
