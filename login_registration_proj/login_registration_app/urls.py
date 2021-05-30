from django.urls import path
from . import views

urlpatterns = [
    #### Login Routes ####
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    #### Wall Routes ####
    path('wall', views.wall),
    path('wall/post_message', views.post_message),
    path('wall/comment/<int:id>', views.comment),
    path('wall/delete/<int:id>', views.delete),
]
