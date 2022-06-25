from django.urls import path 
from . import views


urlpatterns = [
    path('', views.todoList, name='index'),
    path('add/', views.addTodo, name='add'),
]
