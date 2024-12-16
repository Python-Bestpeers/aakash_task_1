from django.contrib import admin

from .models import Comment, Task, User

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(User)
