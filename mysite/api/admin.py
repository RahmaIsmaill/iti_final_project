from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (None, {'fields': ('phone',)}),
    )
