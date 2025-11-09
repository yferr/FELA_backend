
from django.db import connection

from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico para información del usuario.
    """
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'organismo', 'is_approved', 'is_superuser', 'is_staff',
            'created_at'
        ]
        read_only_fields = ['id', 'is_approved', 'is_superuser', 'is_staff', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de nuevos usuarios.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirmar contraseña"
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'organismo'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """Valida que las contraseñas coincidan"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        return attrs

    def validate_email(self, value):
        """Valida que el email no esté registrado"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Ya existe un usuario con este email."
            )
        return value

    def create(self, validated_data):
        """Crea el usuario con contraseña encriptada"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.is_approved = False  # Requiere aprobación del superusuario
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuarios.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Valida las credenciales del usuario"""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Autenticar usuario
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "Usuario o contraseña incorrectos.",
                    code='authorization'
                )

            # Verificar si el usuario está aprobado
            if not user.is_approved:
                raise serializers.ValidationError(
                    "Tu cuenta está pendiente de aprobación por el administrador.",
                    code='not_approved'
                )

            # Verificar si el usuario está activo
            if not user.is_active:
                raise serializers.ValidationError(
                    "Esta cuenta ha sido desactivada.",
                    code='inactive'
                )

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Debes proporcionar usuario y contraseña.",
                code='required'
            )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña.
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """Valida que la contraseña actual sea correcta"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "La contraseña actual es incorrecta."
            )
        return value

    def validate(self, attrs):
        """Valida que las contraseñas nuevas coincidan"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas no coinciden."
            })
        return attrs

    def save(self, **kwargs):
        """Cambia la contraseña del usuario"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar información del usuario.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'organismo']

    def validate_email(self, value):
        """Valida que el email no esté usado por otro usuario"""
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                "Ya existe un usuario con este email."
            )
        return value


class UserApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer para que el superusuario apruebe usuarios.
    Solo el superusuario puede usar este serializer.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'organismo', 'is_approved', 'is_active']
        read_only_fields = ['id', 'username', 'email', 'first_name', 
                           'last_name', 'organismo']