from django.contrib import admin

from .models import CustomUser


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
