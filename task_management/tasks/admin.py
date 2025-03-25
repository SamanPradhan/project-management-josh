from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'mobile', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'mobile')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'mobile')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)
