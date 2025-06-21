from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/edit/<int:pk>/', views.article_edit, name='article_edit'),
    path('articles/delete/<int:pk>/', views.article_delete, name='article_delete'),
]