import json
from django.shortcuts import render
from django.http import JsonResponse
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
    return render(request, 'index.html', {'todos': todos, "todo_list": todo_list})


def todoList(request):
    user_list = user_list_init(request)
    todo_lists = user_list.todoLists.all()
    print(todo_lists)
    return render(request, 'list.html', {'todo_lists': todo_lists})


def addTodo(request):
    if request.method == 'GET':
        data = json.loads(request.GET.get('data'))
        user_list = user_list_init(request)
        slug = data['todo_list_slug']
        title = data['title']
        memo = data['memo']
        important = data['important']
        starred = data['starred']
        datacompleted = data['dateCompleted']
        print(slug)
        print(title)
        print(memo)
        print(important)
        print(starred)
        print(datacompleted)
        todo_list = TodoList.objects.get(users=user_list, slug=slug)
        todo = Todo.objects.create(title=title, memo=memo, important=important, starred=starred)
        todo.save()
        print(todo)
        todo_list.todos.add(todo)
        return JsonResponse({'status': 200, 'title': todo.title, 'id': todo.id})
        # todo_list = TodoList.objects.get(users=user_list,slug=slug)
        # todo_list = user_list.TodoLists.get(slug=slug) 
        # for todosss in user_list.todoLists.all():
            # print('User list', todosss)
            # t = todosss.objects.get(slug=slug)
            # print(t)
        # print('user list', user_list.todoLists.all)
        # todo = Todo(title=title, memo=memo, important=important, starred=starred, datecompleted=datacompleted)
        # todo_list.todos.add(todo)
        # todo.save()