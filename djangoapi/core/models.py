from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Usuario extendido con información adicional.
    Incluye el campo 'organismo' sin relación con la tabla agencies.
    """
    organismo = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Organismo al que pertenece",
        help_text="Organización o institución del usuario"
    )
    
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Usuario aprobado",
        help_text="El superusuario debe aprobar al usuario para que pueda crear/editar datos"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-created_at']

    def __str__(self):
        if self.get_full_name():
            return f"{self.username} ({self.get_full_name()})"
        return self.username

    def save(self, *args, **kwargs):
        # Si es superusuario, aprobar automáticamente
        if self.is_superuser:
            self.is_approved = True
        super().save(*args, **kwargs)