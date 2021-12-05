from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('logs/', views.logs, name='logs'),
    path('logs/<f_name>', views.log, name='log'),
    path('config/<module>', views.config, name='config'),
    path('config/<module>/write', views.write_config, name='write_config')
]
