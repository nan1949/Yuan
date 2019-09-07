"""Defines URL patterns for poems"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author, name='author'),
    path('authors/<int:author_id>/<int:poem_id>/', views.poem, name='poem'),
    path('new_author/', views.new_author, name='new_author'),
    path('new_poem/<int:author_id>/', views.new_poem, name='new_poem'),
    path('new_translation/<int:author_id>/<int:poem_id>/', views.new_translation, name='new_translation'),
    path('edit_poem/<int:poem_id>/', views.edit_poem, name='edit_poem'),
]