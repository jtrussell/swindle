from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'discord_handle')


admin.site.register(UserProfile, UserProfileAdmin)
