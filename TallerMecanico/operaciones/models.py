from django.db import models
from django.contrib.auth.models import User
from core.models import ZonaTrabajo,PerfilUsuario
from core.validators import validar_caracteres_especiales,validar_solo_texto,validar_texto_numeros

class Cliente(models.Model):
    nombre=models.CharField(max_length=120)
    rut=models.CharField(max_length=12,blank=True)
    activo=models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    marca=models.CharField(max_length=120)
    modelo=models.CharField(max_length=120)
    patente = models.CharField(max_length=10, unique=True)
    activo=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patente}"

class OrdenTrabajo(models.Model):
    
    ESTADOS=[
        ("Pendiente","Pendiente"),
        ("En Proceso","En Proceso"),
        ("Finalizado","Finalizado")
    ]
    
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    vehiculo=models.ForeignKey(Vehiculo,on_delete=models.CASCADE)
    descripcion=models.TextField()
    zona=models.ForeignKey(ZonaTrabajo, on_delete=models.SET_NULL, null=True, blank=True)
    mecanico=models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado=models.CharField(max_length=20,choices=ESTADOS,default="Pendiente")
    fecha_inicio=models.DateTimeField(blank=True, null=True)
    fecha_fin=models.DateTimeField(blank=True, null=True)

    creado=models.DateTimeField(auto_now_add=True)
    actualizado=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OT {self.pk} - {self.vehiculo.patente}"    





