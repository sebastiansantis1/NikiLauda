from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registrar_trabajo, name="registrar_trabajo"),
    path("trabajos/", views.lista_trabajos, name="lista_trabajos"),
    path("trabajo/<int:pk>/", views.detalle_trabajo, name="detalle_trabajo"),
    path("crear-cliente/", views.crear_cliente, name="crear_cliente"),
    path("crear-vehiculo/", views.crear_vehiculo, name="crear_vehiculo"),
    path("editar/<int:pk>/", views.editar_trabajo, name="editar_trabajo"),

]