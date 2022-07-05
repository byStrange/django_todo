from django.shortcuts import redirect
from django.urls import path 
from . import views

app_name = 'todo'

urlpatterns = [
    path('lists/', views.todoList, name='index'),
    path('change/', views.changeTodo, name='add'),
]
