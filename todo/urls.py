from django.urls import path 
from . import views


urlpatterns = [
    path('', views.todoList, name='index'),
    path('change/', views.changeTodo, name='add'),
]
