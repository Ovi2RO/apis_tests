from django.contrib import admin

# Register your models here.
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "phone_number",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields":("phone_number",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields":("phone_number",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)