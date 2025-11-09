#Django imports
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import CustomUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UserUpdateSerializer,
    UserApprovalSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint para obtener el CSRF token.
    Útil para aplicaciones frontend que usan autenticación por sesión.
    """
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Endpoint para registro de nuevos usuarios.
    El usuario queda pendiente de aprobación por el superusuario.
    
    POST /api/auth/register/
    Body:
    {
        "username": "usuario123",
        "email": "usuario@example.com",
        "password": "contraseña_segura",
        "password2": "contraseña_segura",
        "first_name": "Juan",
        "last_name": "Pérez",
        "organismo": "CSIC"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "Usuario registrado exitosamente. Tu cuenta está pendiente de aprobación por el administrador.",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint para login de usuarios.
    Utiliza autenticación por sesión de Django.
    
    POST /api/auth/login/
    Body:
    {
        "username": "usuario123",
        "password": "contraseña_segura"
    }
    """
    serializer = LoginSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        return Response(
            {
                "message": "Login exitoso",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint para logout de usuarios.
    Cierra la sesión actual.
    
    POST /api/auth/logout/
    """
    logout(request)
    return Response(
        {"message": "Logout exitoso"},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Endpoint para obtener información del usuario actual.
    
    GET /api/auth/user/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    """
    Endpoint para actualizar información del usuario actual.
    
    PUT/PATCH /api/auth/user/update/
    Body:
    {
        "first_name": "Juan Carlos",
        "last_name": "Pérez García",
        "email": "nuevo_email@example.com",
        "organismo": "UNESCO"
    }
    """
    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=(request.method == 'PATCH'),
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Información actualizada exitosamente",
                "user": UserSerializer(request.user).data
            },
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Endpoint para cambiar la contraseña del usuario actual.
    
    POST /api/auth/change-password/
    Body:
    {
        "old_password": "contraseña_actual",
        "new_password": "nueva_contraseña",
        "new_password2": "nueva_contraseña"
    }
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Contraseña cambiada exitosamente"},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios (solo superusuarios).
    Permite listar, ver detalle, aprobar y desactivar usuarios.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action in ['approve', 'toggle_active']:
            return UserApprovalSerializer
        return UserSerializer

    def get_queryset(self):
        """Filtros opcionales para buscar usuarios"""
        queryset = CustomUser.objects.all().order_by('-created_at')
        
        # Filtrar por estado de aprobación
        is_approved = self.request.query_params.get('is_approved')
        if is_approved is not None:
            is_approved_bool = is_approved.lower() == 'true'
            queryset = queryset.filter(is_approved=is_approved_bool)
        
        # Filtrar por estado activo
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        # Buscar por username, email o nombre
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        
        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Aprueba un usuario pendiente.
        
        POST /api/auth/users/{id}/approve/
        """
        user = self.get_object()
        
        if user.is_approved:
            return Response(
                {"message": "El usuario ya está aprobado"},
                status=status.HTTP_200_OK
            )
        
        user.is_approved = True
        user.save()
        
        return Response(
            {
                "message": f"Usuario {user.username} aprobado exitosamente",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Activa o desactiva un usuario.
        
        POST /api/auth/users/{id}/toggle_active/
        """
        user = self.get_object()
        
        # No permitir desactivar al superusuario actual
        if user == request.user and user.is_superuser:
            return Response(
                {"error": "No puedes desactivar tu propia cuenta de superusuario"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = not user.is_active
        user.save()
        
        action_text = "activado" if user.is_active else "desactivado"
        
        return Response(
            {
                "message": f"Usuario {user.username} {action_text} exitosamente",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Lista usuarios pendientes de aprobación.
        
        GET /api/auth/users/pending/
        """
        pending_users = CustomUser.objects.filter(
            is_approved=False
        ).order_by('-created_at')
        
        serializer = UserSerializer(pending_users, many=True)
        return Response({
            "count": pending_users.count(),
            "users": serializer.data
        })



#
#from django.http import JsonResponse
#from django.views import View
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.shortcuts import redirect
#import random, time
#def custom_logout_view(request):
#    logout(request)
#    return redirect("/accounts/login/")  # O a donde desees redirigir después del logout
#
#def notLoggedIn(request):
#    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]})
#
#class HelloWord(View):
#    def get(self, request):
#        return JsonResponse({"ok":True,"message": "Core. Hello world", "data":[]})
#
#class LoginView(View):
#    def post(self, request, *args, **kwargs):
#        if request.user.is_authenticated:
#            username=request.user.username
#            return JsonResponse({"ok":True,"message": "The user {0} already is authenticated".format(username), "data":[{'username':request.user.username}]})
#
#        username=request.POST.get('username')
#        password=request.POST.get('password')
#        user = authenticate(username=username, password=password)
#        if user:
#            login(request,user)#introduce into the request cookies the session_id,
#                    # and in the auth_sessions the session data. This way, 
#                    # in followoing requests, know who is the user and if
#                    # he is already authenticated. 
#                    # The coockies are sent in the response header on POST requests
#            return JsonResponse({"ok":True,"message": "User {0} logged in".format(username), "data":[{"username": username}]})
#        else:
#            # To make thinks difficult to hackers, you make a random delay,
#            # between 0 and 1 second
#            seconds=random.uniform(0, 1)
#            time.sleep(seconds)
#            return JsonResponse({"ok":False,"message": "Wrong user or password", "data":[]})
#
#class LogoutView(LoginRequiredMixin, View):
#    def post(self, request, *args, **kwargs):
#        username=request.user.username
#        logout(request) #removes from the header of the request
#                            #the the session_id, stored in a cookie
#        return JsonResponse({"ok":True,"message": "The user {0} is now logged out".format(username), "data":[]})
#
#
#class IsLoggedIn(View):
#    def post(self, request, *args, **kwargs):
#        print(request.user.username)
#        print(request.user.is_authenticated)
#        if request.user.is_authenticated:
#            return JsonResponse({"ok":True,"message": "You are authenticated", "data":[{'username':request.user.username}]})
#        else:
#            return JsonResponse({"ok":False,"message": "You are not authenticated", "data":[]})
