from django.contrib import admin
from .models import User, UsersToDocs


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')


@admin.register(UsersToDocs)
class UsersToDocsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doc')
    search_fields = ('user__username', 'doc__file_path')
    list_filter = ('user',)


