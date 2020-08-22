from django.urls import path

from . import views

urlpatterns = [
    path('random-entry', views.random_entry, name='random-entry'),
    path('edit/<str:title>', views.edit, name='edit'),
    path('new-page', views.new_page, name='new-page'),
    path('search', views.search, name='search'),
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name='entry')
]
