from django.contrib import admin

from .models import CustomUser, Subscribe


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'email',
        'username',
    )
    search_fields = (
        'email',
        'username',
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    list_filter = (
        'user',
        'author'
    )
    search_fields = (
        'user',
        'author'
    )
