from django.contrib import admin
from .models import UserProfile, CustomUser, Role


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','role', 'date_joined']
    list_filter = ['date_joined']
    search_fields = ['username', 'email']



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['user']



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
