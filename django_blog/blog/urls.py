from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    # General User Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # OPTION A: Match the default Django redirect for profile
    path('accounts/profile/', views.profile, name='profile'), # Modified line

    # Home and Post Listing
    path('', views.home_view, name='home'),
    path('posts/', views.PostListView.as_view(), name='posts'),

    # Individual Post URLs
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs (nested under post for creation)
    path('post/<int:pk>/comment/new/', views.CommentCreateView.as_view(), name='comment_new'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # Tag and Search URLs
    path('tags/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('search/', views.post_search, name='post_search'),
    path('privacy/', views.privacy_policy_view, name='privacy'),
]
