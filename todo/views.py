import json
from django.shortcuts import render
from django.http import JsonResponse
from todo.models import *
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
# import authenticated, 


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
    lengthOfDoneTodos = len(todos.filter(done=True))
    return render(request, 'index.html', {'todos': todos, "todo_list": todo_list, "lengthOfDoneTodos": lengthOfDoneTodos})


def todoList(request):
    if request.user.is_authenticated:
        user_list = user_list_init(request)
        todo_lists = user_list.todoLists.all()
        return render(request, 'list.html', {'todo_lists': todo_lists})
    else:
        return render(request, 'login.html')


def changeTodo(request):
    if request.method == 'GET':
        data = json.loads(request.GET.get('data'))
        user_list = user_list_init(request)
        if data['action'] == "C":
            if data['do'] == 'create_list':
                todo_list = TodoList(
                    title=data['title'], slug=data['slug'], memo=data['memo'], created=datetime.now())
                todo_list.save()
                user_list.addTodoList(todo_list)
                return JsonResponse({'status': 'success', 'response': {'ok': True,'slug': todo_list.slug, 'title': todo_list.title, 'id': todo_list.id, 'memo': todo_list.memo, 'created': todo_list.created}})
            slug = data['todo_list_slug']
            title = data['title']
            memo = data['memo']
            important = data['important']
            starred = data['starred']
            todo_list = TodoList.objects.get(users=user_list, slug=slug)
            todo = Todo.objects.create(
                title=title, memo=memo, important=important, starred=starred)
            todo.save()
            todo_list.addTodo(todo)
            return JsonResponse({'ok': True, 'title': todo.title, 'id': todo.id})
        elif data['action'] == "U":
            todo_id = data['id']
            todo = Todo.objects.get(id=todo_id)

            response = {
                "id": todo.id,
                'title': todo.title,
                "memo": todo.memo,
                "important": todo.important,
                'starred': todo.starred,
            }
            print(data['do'])
            if data['do'] == 'mark':
                todo.done = True
                todo.datecompleted = datetime.now()
                todo.save()
                response['done'] = True
                response['datecompleted'] = todo.datecompleted
            elif data['do'] == 'unmark':
                todo.done = False
                todo.save()
                response['done'] = False
            return JsonResponse({"ok": True, "response": response})
