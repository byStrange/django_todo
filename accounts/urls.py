from django.urls import path
from todo import views

app_name = 'accounts'


urlpatterns = [
    path('<str:user_name>/', views.profileView, name='profile'),
    path('<str:user>/lists/', views.todoList, name="lists"),
    path('<str:user>/list/<str:slug>/', views.todoListDetail, name="list"),
    path('<str:user>/followers/', views.followers, name="followers"),
    path('<str:user>/following/', views.following, name="following"),
    path('<str:user_name>/follow/', views.follow, name="follow"),
    path('<str:user_name>/unfollow/', views.unfollow, name="follow"),
    path('<str:user_name>/tasks/', views.allTodosView, name="todos"),
    path('<str:user_name>/edit/', views.userEdit, name="todos"),
]