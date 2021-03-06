from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    todoLists = models.ManyToManyField('TodoList', related_name='users', blank=True)
    todos = models.ManyToManyField('Todo', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, default='profile_photos/default.svg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


    def addTodoList(self, todoList):
        self.todoLists.add(todoList)
        
    def addTodo(self, todo):
        self.todos.add(todo)


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    todos = models.ManyToManyField('Todo', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    private = models.BooleanField(default=False)

    def addTodo(self, todo):
        self.todos.add(todo)
    

    def __str__(self):
        return self.title


class Todo(models.Model):
    PRIORITY = (
        ('primary', 'default'),
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('success', 'success'),
    )

    title = models.CharField(max_length=50)
    memo = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY, default='primary', blank=True, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title


    def lengthOfDone(self):
        return len(self.todos.filter(done=True))