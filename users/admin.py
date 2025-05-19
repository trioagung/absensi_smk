from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'nama_lengkap']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'nama_lengkap', 'jurusan', 'kelas')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'nama_lengkap', 'jurusan', 'kelas')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)