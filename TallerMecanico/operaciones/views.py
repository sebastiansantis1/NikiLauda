from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import OrdenTrabajoForm
from .models import OrdenTrabajo, Cliente, Vehiculo
from core.models import PerfilUsuario


# ---------------------------------------------------------
#   HU002 - Registrar Trabajo
# ---------------------------------------------------------
@login_required
def registrar_trabajo(request):
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_trabajos")
    else:
        form = OrdenTrabajoForm()

    return render(request, "operaciones/registrar_trabajo.html", {"form": form})


# ---------------------------------------------------------
#   HU003 - Lista de Trabajos
# ---------------------------------------------------------
@login_required
def lista_trabajos(request):
    trabajos = OrdenTrabajo.objects.all().order_by("-creado")
    return render(request, "operaciones/lista_trabajos.html", {"trabajos": trabajos})


# ---------------------------------------------------------
#   Detalle de un Trabajo
# ---------------------------------------------------------
@login_required
def detalle_trabajo(request, pk):
    trabajo = get_object_or_404(OrdenTrabajo, pk=pk)
    return render(request, "operaciones/detalle_trabajo.html", {"trabajo": trabajo})


# ---------------------------------------------------------
#   Editar Trabajo (permisos)
# ---------------------------------------------------------
@login_required
def editar_trabajo(request, pk):
    trabajo = get_object_or_404(OrdenTrabajo, pk=pk)
    perfil = request.user.perfil

    if not (
        perfil.rol == "ADMIN"
        or perfil.rol == "ENCARGADO"
        or trabajo.mecanico == perfil
    ):
        return HttpResponse("No tienes permisos para editar este trabajo.", status=403)

    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            return redirect("lista_trabajos")
    else:
        form = OrdenTrabajoForm(instance=trabajo)

    return render(request, "operaciones/editar_trabajo.html", {
        "form": form,
        "trabajo": trabajo
    })


# ---------------------------------------------------------
#   Crear Cliente
# ---------------------------------------------------------
@login_required
def crear_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        rut = request.POST.get("rut")

        if not nombre:
            return render(request, "operaciones/crear_cliente.html", {
                "errors": "El nombre es obligatorio"
            })

        Cliente.objects.create(nombre=nombre, rut=rut)
        return redirect("registrar_trabajo")

    return render(request, "operaciones/crear_cliente.html")


# ---------------------------------------------------------
#   Crear Vehículo
# ---------------------------------------------------------
@login_required
def crear_vehiculo(request):
    clientes = Cliente.objects.all()

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        patente = request.POST.get("patente")
        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")

        if not patente:
            return render(request, "operaciones/crear_vehiculo.html", {
                "clientes": clientes,
                "errors": "La patente es obligatoria"
            })

        Vehiculo.objects.create(
            cliente_id=cliente_id,
            patente=patente,
            marca=marca,
            modelo=modelo
        )

        return redirect("registrar_trabajo")

    return render(request, "operaciones/crear_vehiculo.html", {"clientes": clientes})
