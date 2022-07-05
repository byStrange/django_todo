
from django.contrib import admin
from django.urls import path, include
from todo.views import profileView, todoListDetail, userRegister, userLogin, index, userLogout


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', index, name='index'),


    path('todo/', include('todo.urls'), name='todo'),

    path('accounts/', include('accounts.urls', namespace='accounts')
         ),    path('register/', userRegister, name='register'),

    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),

]
