from django.shortcuts import render
from todo.models import *

# Create your views here.


def user_list_init(request):
    try:
        user_list = UserList.objects.get(user=request.user)
    except UserList.DoesNotExist:
        user_list = UserList(user=request.user)
        user_list.save()
    return user_list


def todoListDetail(request, slug):
    user_list = user_list_init(request)
    todo_list = user_list.todoLists.get(slug=slug)
    todos = todo_list.todos.all()
    return render(request, 'index.html', {'todos': todos, "todo_list_name": todo_list.title})


def todoList(request):
    user_list = user_list_init(request)
    todo_lists = user_list.todoLists.all()
    print(todo_lists)
    return render(request, 'list.html', {'todo_lists': todo_lists})


def addTodo(request):
    if request.method == 'POST':
        user_list = user_list_init(request)
        todo_list = user_list.todoLists.get(slug=request.POST.get('todo_list_slug')) 
        print(request.POST)
        todo = Todo(title=request.POST.get('title'), memo=request.POST.get('memo'), important=request.POST.get('important'), starred=request.POST.get('starred'), datecompleted=request.POST.get('datecompleted'))
        todo_list.todos.add(todo)
        todo.save()
        return render(request, 'index.html', {'todos': todo_list.todos.all(), "todo_list_name": todo_list.title})