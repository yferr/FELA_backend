from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    get_csrf_token,
    register_view,
    login_view,
    logout_view,
    current_user_view,
    update_user_view,
    change_password_view,
    UserManagementViewSet
)

# Router para el ViewSet de gestión de usuarios
router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='user-management')

urlpatterns = [
    # CSRF Token
    path('csrf/', get_csrf_token, name='csrf'),
    
    # Autenticación básica
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Usuario actual
    path('user/', current_user_view, name='current-user'),
    path('user/update/', update_user_view, name='update-user'),
    path('change-password/', change_password_view, name='change-password'),
    
    # Gestión de usuarios (solo admin)
    path('', include(router.urls)),
]