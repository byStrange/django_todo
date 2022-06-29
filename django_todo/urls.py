from django.contrib import admin
from django.urls import path, include
from todo.views import todoListDetail, todoList, userRegister, userLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todoList, name='index'),
    path('list/<str:slug>/', todoListDetail, name='list'),

    path('todo/', include('todo.urls')),

    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
]