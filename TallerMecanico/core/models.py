from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class ZonaTrabajo(models.Model):
    """Zona física del taller donde se realizan reparaciones."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    """Extensión del usuario Django para roles y datos adicionales."""

    ROLES = [
        ("ADMIN", "Administrador"),
        ("MECANICO", "Mecánico"),
        ("ENCARGADO", "Encargado del Taller"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=ROLES, default="MECANICO")

    # Eliminado: ocupada (ese campo es de ZONA)
    activo = models.BooleanField(default=True)
    rut = models.CharField(max_length=12, unique=True)

    ultimo_movimiento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"


class ConfiguracionSistema(models.Model):
    """Parámetros configurables del sistema."""
    clave = models.CharField(max_length=100, unique=True)
    valor = models.CharField(max_length=500, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.clave}: {self.valor}"
