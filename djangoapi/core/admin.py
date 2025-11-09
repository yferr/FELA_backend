from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuración del panel de administración para CustomUser.
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'organismo', 'is_approved', 'is_active', 'is_staff',
        'is_superuser', 'created_at'
    ]
    
    list_filter = [
        'is_approved', 'is_active', 'is_staff', 'is_superuser',
        'created_at'
    ]
    
    search_fields = [
        'username', 'email', 'first_name', 'last_name', 'organismo'
    ]
    
    ordering = ['-created_at']
    
    # Campos editables en la lista
    list_editable = ['is_approved', 'is_active']
    
    # Campos mostrados en el formulario de detalle
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('organismo', 'is_approved', 'created_at', 'updated_at')
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ['created_at', 'updated_at']
    
    # Campos para agregar usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'first_name', 'last_name', 'organismo', 'is_approved')
        }),
    )
    
    # Acciones personalizadas
    actions = ['approve_users', 'disapprove_users']
    
    @admin.action(description='Aprobar usuarios seleccionados')
    def approve_users(self, request, queryset):
        """Aprueba múltiples usuarios"""
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} usuario(s) aprobado(s) exitosamente.')
    
    @admin.action(description='Desaprobar usuarios seleccionados')
    def disapprove_users(self, request, queryset):
        """Desaprueba múltiples usuarios"""
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} usuario(s) desaprobado(s) exitosamente.')