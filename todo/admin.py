from django.contrib import admin
from todo.models import (TodoList, Todo, UserList)

# prepopluted field for TodoList title field without class


class TodoListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Todo)
admin.site.register(UserList)


# Register your models here.
