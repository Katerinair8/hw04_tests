from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('group/<slug>/', views.group_posts, name='group_posts'),
    path('', views.index, name='index'),
    path('posts/<post_id>/edit/', views.post_edit, name='post_edit'),
    path('create/', views.post_create, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]
