from django.contrib import admin
from server.models import Task, Post, Group, Badge, User, ForgotPasswordRequest

# Register your models here.
admin.site.register(Task)
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Badge)
admin.site.register(User)
admin.site.register(ForgotPasswordRequest)