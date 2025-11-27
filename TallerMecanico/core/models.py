from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class ZonaTrabajo(models.Model): #Esta es la zona fisica de mi taller,
    #lugar donde se realiza la operacion
    
    nombre=models.CharField(max_length=100, unique=True)
    descripcion=models.TextField(blank=True)
    activo=models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    
class PerfilUsuario(models.Model):  # Manejo de roles: admin, mecanico, encargado
    ROLES = [
        ("ADMIN", "Administrador"),
        ("MECANICO", "Mecánico"),
        ("ENCARGADO", "Encargado del Taller"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=ROLES, default="MECANICO")

    activo = models.BooleanField(default=True)
    rut = models.CharField(max_length=12, unique=True)
    ultimo_movimiento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    
class ConfiguracionSistema(models.Model):
    #tabla para manejar perimetros globales de mi sistema 
    
    clave=models.CharField(max_length=100, unique=True)
    valor=models.CharField(max_length=500,blank=True)
    descripcion=models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.clave}: {self.valor}"