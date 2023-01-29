from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


@admin.register(User)
class CustomUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация',
         {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа',
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты',
         {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'password1',
                'password2'
            ),
        }),
    )
    list_filter = ('email', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pub_date')
