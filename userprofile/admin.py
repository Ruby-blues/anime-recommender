from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

# Register your models here.
from .models import User


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff')
    fieldsets = (
        ('User', {'fields': ('email', 'user_name', 'first_name', 'last_name')}),
        ('Personal', {'fields': ('about', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})}
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'first_name', 'last_name', 'about',
                       'profile_pic', 'is_active', 'is_superuser', 'is_staff', )}
         ),
    )


admin.site.register(User, UserAdminConfig)
