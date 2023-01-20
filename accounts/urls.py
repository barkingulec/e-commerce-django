from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register"),
    path('dashboard/', views.user_dashboard, name="dashboard"),
    path('logout/', views.user_logout, name="logout"),
    path('add_to_favorite/', views.add_to_favorite, name="add_to_favorite"),
    path('add_to_liked/', views.add_to_liked, name="add_to_liked"),
    path('remove_from_favorite/', views.remove_from_favorite, name="remove_from_favorite"),
    path('remove_from_liked/', views.remove_from_liked, name="remove_from_liked"),
    path('post_add_to_favorite/', views.post_add_to_favorite, name="post_add_to_favorite"),
    path('post_add_to_liked/', views.post_add_to_liked, name="post_add_to_liked"),
    path('post_remove_from_favorite/', views.post_remove_from_favorite, name="post_remove_from_favorite"),
    path('post_remove_from_liked/', views.post_remove_from_liked, name="post_remove_from_liked"),
]