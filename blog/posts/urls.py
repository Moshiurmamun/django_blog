from django.urls import path, re_path
from .import views



app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('category/<name>', views.category, name="topic"),
    path('create/', views.post_create, name='create'),
    re_path('edit/(?P<slug>[\w-]+)/', views.post_update, name='post_edit'),
    re_path('delete/(?P<slug>[\w-]+)/', views.post_delete, name="post_delete"),
    re_path('(?P<slug>[\w-]+)/', views.post_detail, name='detail'),




]
