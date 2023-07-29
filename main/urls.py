from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog", views.catalog, name="catalog"),
    path("species/<str:species>", views.species, name="species"),
    path("post", views.post, name="post"),
] 