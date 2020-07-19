from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("search/<str:keyword>", views.searchPage, name="searchPage"),
    path("createPage", views.createPage, name="createPage"),
    path("createAPI", views.createAPI, name="createAPI"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("editAPI", views.editAPI, name="editAPI"),
    path("<str:title>", views.title, name="title")
]
