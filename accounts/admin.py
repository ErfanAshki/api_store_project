from django.contrib import admin


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm, UserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'age', 'is_staff']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'age', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
