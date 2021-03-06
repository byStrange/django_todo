from email import message
import json
from operator import is_
from urllib.parse import uses_netloc
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import JsonResponse
import todo
from todo.models import *
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages


def user_list_init(request):
    try:
        user_list = UserList.objects.get(user=request.user)
    except:
        user_list = UserList(user=request.user)
        user_list.save()
    return user_list


def index(request):
    is_authenticated = False
    if request.user.is_authenticated:
        user_list_init(request)
        is_authenticated = True
    
    return render(request, 'index.html', {'navigation_button': True, 'is_authenticated': is_authenticated} )


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                print(user)
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Wrong password')
                return redirect('/login')
        except:
            messages.error(request, 'User not found')
            return redirect('/login')
    else:
        return render(request, 'login.html')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        print(password, '.', confirm_password, '.')
        if password != confirm_password:
            messages.error(request, 'Password did\'nt match')
            return redirect('/register')
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        try:
            user = User.objects.get(username=username)
            messages.error(
                request, 'This username is already taken, choose another one!')
            return redirect('/register')
        except:
            user = User.objects.create(
                username=username,  email=email, first_name=name, last_name=surname)
            user.set_password(password) # for hashing password
        user.save()
        login(request, user)
        user_list_init(request)
        return redirect('/')
    else:
        return render(request, 'register.html')

def userEdit(request, user_name): 
    if request.user.is_authenticated:
        user_list = UserList.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        data = request.POST
        if data:
            # if users new username is existent, return error
            if User.objects.filter(username=data['username']).exists():
                messages.error(request, 'This username is already taken, choose another one!')
                return redirect('/accounts/' + str(request.user.username))
            else:
                user.username = data['username']
            # if users new email is existent, return error
            if User.objects.filter(email=data['email']).exists():
                messages.error(request, 'This email is already taken, choose another one!')
                return redirect('/accounts/' + str(request.user.username) + '/')
            else:
                user.email = data.get('email')
            user_list.bio = data.get('bio')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.save()
            messages.success(request, 'Account updated')
            return redirect('/accounts/' + str(request.user.username) + '/')
        else:
            return render(request, 'profile.html')

def followers(request, user):
    if request.user.is_authenticated:
        _user = User.objects.get(username=user)
        user_list = UserList.objects.get(user=_user)
        followers = user_list.followers.all()
        print(user_list)
        print(request.user)
        if request.user in user_list.followers.all():
            print('true')

        return render(request, 'followers.html', {'followers': followers, 'user': _user})
    else:
        return render(request, 'login.html')


def following(request, user):
    if request.user.is_authenticated:
        _user = User.objects.get(username=user)
        user_list = UserList.objects.get(user=_user)
        following = user_list.following.all()
        return render(request, 'following.html', {'following': following, 'user': _user})
    else:
        return render(request, 'login.html')


def follow(request, user_name):
    if request.user.is_authenticated:
        if request.user.username != user_name:
            user = User.objects.get(username=user_name)
            follower_user = User.objects.get(username=request.user.username)

            follower = UserList.objects.get(user=follower_user)
            following = UserList.objects.get(user=user)
            
            following.followers.add(follower_user)
            follower.following.add(user)
            return JsonResponse({'status': 'success'})

        else:
            print('cannot follow yourself')
            messages.error(request, 'You cannot follow yourself')
            return redirect('/')


def unfollow(request, user_name):
    if request.user.is_authenticated:
        if request.user.username != user_name:
            user = User.objects.get(username=user_name)
            follower_user = User.objects.get(username=request.user.username)

            follower = UserList.objects.get(user=follower_user)
            following = UserList.objects.get(user=user)
            
            following.followers.remove(follower_user)
            follower.following.remove(user)
            return JsonResponse({'status': 'success', 'follower': follower.user.username})

        else:
            print('cannot follow yourself')
            messages.error(request, 'You cannot follow yourself')
            return redirect('/')


def userLogout(request):
    logout(request)
    return redirect('/')


def profileView(request, user_name):
    if request.user.is_authenticated:
        user = User.objects.get(username=user_name)
        user_list = UserList.objects.get(user=user)
        if request.user.username == user_name:
            todo_lists = user_list.todoLists.all()
        else:
            todo_lists = user_list.todoLists.all().filter(private=False)
        is_verified = False
        if user_list.user.is_superuser:
            is_verified = True
        todos = user_list.todos.all()
        if request.user.username == user_name:
            print(user_list.bio)
            return render(request, 'profile.html', {'todo_lists': todo_lists, 'todos': todos, 'user': user_list, 'owner': True, 'is_verified': is_verified})
        else:
            try:
                user = User.objects.get(username=user_name)
                user_list = UserList.objects.get(user=user)
                visitor = User.objects.get(username=request.user.username)
                followed = False
                if visitor in user_list.followers.all():
                    # if request.user has already followed this user (user_name)
                    followed = True
                if request.user.username == user:
                    todo_lists = user_list.todoLists.all()
                else:
                    todo_lists = user_list.todoLists.all().filter(private=False)
                todos = user_list.todos.all()
                print('you are viewing this user', user)
                return render(request, 'profile.html', {'todo_lists': todo_lists, 'todos': todos, 'user': user_list, 'owner': False, 'is_verified': is_verified, 'followed': followed})
            except:
                messages.error(request, 'User not found')
                return redirect('/')
    else:
        return render(request, 'login.html')

def allTodosView(request, user_name):
    if request.user.is_authenticated:
        user = User.objects.get(username=user_name)
        todos = UserList.objects.get(user=user).todos.all()
        if request.user.username == user_name:
            isEmpty = todos.count() == 0
        else:
            isEmpty = todos.filter(private=False).count() == 0
        print({'viewer': request.user,'todos': todos, 'user': user, 'isEmpty': isEmpty})
        return render(request, 'todos.html', {'todos': todos, 'user': user, 'isEmpty': isEmpty})
    else:
        return render(request, 'login.html')


def todoListDetail(request, slug, user):
    _user = User.objects.get(username=user)
    user_list = UserList.objects.get(user=_user)
    todo_list = user_list.todoLists.get(slug=slug)
    todos = todo_list.todos.all()
    lengthOfDoneTodos = len(todos.filter(done=True))
    if request.user.username == user:
        isEmpty = todos.count() == 0
        return render(request, 'todo_details.html', {'todos': todos, "todo_list": todo_list, "lengthOfDoneTodos": lengthOfDoneTodos, 'isEmpty': isEmpty})
    else:
        isEmpty = todos.filter(private=False).count() == 0
        return render(request, 'todos.html', {'todos': todos, 'user': _user, 'isEmpty': isEmpty, 'todo_list': todo_list})

def todoList(request, user):
    if request.user.is_authenticated:
        user_lists = UserList.objects.all()
        for user_list in user_lists:
            if user_list.user.username == user:
                if request.user.username == user:
                    todo_list = user_list.todoLists.all()
                else:
                    todo_list = user_list.todoLists.all().filter(private=False)
        return render(request, 'list.html', {'todo_lists': todo_list, 'user': user})
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
                return JsonResponse({'status': 'success', 'response': {'ok': True, 'slug': todo_list.slug, 'title': todo_list.title, 'id': todo_list.id, 'memo': todo_list.memo, 'created': todo_list.created}})
            slug = data['todo_list_slug']
            title = data['title']
            memo = data['memo']
            important = data['important']
            starred = data['starred']
            todo = Todo.objects.create(
                title=title, memo=memo, important=important, starred=starred)
            todo.save()
            print(slug)
            if slug:
                todo_list = TodoList.objects.get(users=user_list, slug=slug)
                todo_list.addTodo(todo)
            user_list.addTodo(todo)
            return JsonResponse({'ok': True, 'title': todo.title, 'id': todo.id})
        elif data['action'] == "U":
            if data['do'] == 'rename_todo':
                todo = Todo.objects.get(id=data['id'])
                todo.title = data['title']
                todo.memo = data['memo']
                todo.save()
                return JsonResponse({'status': 'success', 'title': todo.title, 'id': todo.id})
            if data['do'] == 'like_todo':
                todo = Todo.objects.get(id=data['id'])
                todo.important = data['important']
                todo.save()
                return JsonResponse({'status': 'success', 'important': todo.important, 'id': todo.id})
            todo_id = data['id']
            todo = Todo.objects.get(id=todo_id)

            response = {
                "id": todo.id,
                'title': todo.title,
                "memo": todo.memo,
                "important": todo.important,
                'starred': todo.starred,
            }
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
        elif data['action'] == "D":
            if data['do'] == 'delete_todo':
                todo = Todo.objects.get(id=data['id'])
                todo.delete()
                return JsonResponse({'status': 'success', 'id': data['id']})