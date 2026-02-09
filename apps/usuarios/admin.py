from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'es_profesor')
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Academia', {'fields': ('es_profesor', 'bio')}),
    )
