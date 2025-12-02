from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import OrdenTrabajoForm
from .models import OrdenTrabajo, Cliente, Vehiculo, HistorialTrabajo
from core.models import ZonaTrabajo

# ---------------------------------------------------------
#   Registrar Trabajo
# ---------------------------------------------------------
@login_required
def registrar_trabajo(request):

    # 1. MECÁNICOS DISPONIBLES
    mecanicos_ocupados = OrdenTrabajo.objects.filter(
        estado__in=["Pendiente", "En Proceso"]
    ).values_list("mecanico_id", flat=True)

    from core.models import PerfilUsuario
    mecanicos_disponibles = PerfilUsuario.objects.filter(
        rol="MECANICO",
        activo=True
    ).exclude(id__in=mecanicos_ocupados)

    # 2. ZONAS DISPONIBLES
    zonas_ocupadas = OrdenTrabajo.objects.filter(
        estado__in=["Pendiente", "En Proceso"]
    ).values_list("zona_id", flat=True)

    zonas_disponibles = ZonaTrabajo.objects.filter(
        activo=True
    ).exclude(id__in=zonas_ocupadas)

    # 3. PROCESAR FORMULARIO
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST)
        form.fields["mecanico"].queryset = mecanicos_disponibles
        form.fields["zona"].queryset = zonas_disponibles

        if form.is_valid():
            trabajo = form.save()
            return redirect("detalle_trabajo", pk=trabajo.pk)

    else:
        form = OrdenTrabajoForm()
        form.fields["mecanico"].queryset = mecanicos_disponibles
        form.fields["zona"].queryset = zonas_disponibles

    return render(request, "operaciones/registrar_trabajo.html", {
        "form": form,
        "mecanicos_disponibles": mecanicos_disponibles,
        "zonas_disponibles": zonas_disponibles
    })


# ---------------------------------------------------------
#   Lista de Trabajos
# ---------------------------------------------------------
@login_required
def lista_trabajos(request):
    estado = request.GET.get("estado")
    trabajos = OrdenTrabajo.objects.all().order_by("-creado")

    if estado in ["Pendiente", "En Proceso", "Finalizado"]:
        trabajos = trabajos.filter(estado=estado)

    return render(request, "operaciones/lista_trabajos.html", {
        "trabajos": trabajos,
        "filtro": estado
    })


# ---------------------------------------------------------
#   Detalle de un Trabajo + HISTORIAL
# ---------------------------------------------------------
@login_required
def detalle_trabajo(request, pk):
    trabajo = get_object_or_404(OrdenTrabajo, pk=pk)

    historial = HistorialTrabajo.objects.filter(
        trabajo=trabajo
    ).order_by("-fecha")

    return render(request, "operaciones/detalle_trabajo.html", {
        "trabajo": trabajo,
        "historial": historial
    })


# ---------------------------------------------------------
#   Editar Trabajo
# ---------------------------------------------------------
@login_required
def editar_trabajo(request, pk):
    trabajo = get_object_or_404(OrdenTrabajo, pk=pk)
    perfil = request.user.perfil

    # Permisos
    if perfil.rol not in ["ADMIN", "ENCARGADO"] and trabajo.mecanico != perfil:
        return HttpResponse("No tienes permisos para editar este trabajo.", status=403)

    # Guardar valores originales
    estado_anterior = trabajo.estado
    zona_anterior = trabajo.zona
    mecanico_anterior = trabajo.mecanico
    descripcion_anterior = trabajo.descripcion
    fecha_anterior = trabajo.fecha_inicio

    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()

            cambios = []

            if estado_anterior != trabajo.estado:
                cambios.append(f"Estado cambiado de {estado_anterior} a {trabajo.estado}")

            if zona_anterior != trabajo.zona:
                cambios.append(f"Zona cambiada de {zona_anterior} a {trabajo.zona}")

            if mecanico_anterior != trabajo.mecanico:
                cambios.append(f"Mecánico cambiado de {mecanico_anterior} a {trabajo.mecanico}")

            if descripcion_anterior != trabajo.descripcion:
                cambios.append("Descripción del problema modificada")

            if fecha_anterior != trabajo.fecha_inicio:
                cambios.append(
                    f"Fecha cambiada de {fecha_anterior} a {trabajo.fecha_inicio}"
                )

            # Registrar historial
            for c in cambios:
                HistorialTrabajo.objects.create(
                    trabajo=trabajo,
                    descripcion=c,
                    usuario=request.user,
                )

            return redirect("detalle_trabajo", pk=trabajo.pk)

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


# ---------------------------------------------------------
#   Cargar Vehículos vía AJAX
# ---------------------------------------------------------
def cargar_vehiculos(request):
    cliente_id = request.GET.get("cliente")
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values("id", "patente")
    return JsonResponse(list(vehiculos), safe=False)


# ---------------------------------------------------------
#   Trabajos en Progreso
# ---------------------------------------------------------
@login_required
def trabajos_en_progreso(request):
    trabajos = OrdenTrabajo.objects.filter(
        estado__in=["Pendiente", "En Proceso"]
    ).order_by("-creado")

    return render(request, "operaciones/trabajos_en_progreso.html", {
        "trabajos": trabajos
    })


# ---------------------------------------------------------
#   Dashboard Encargado
# ---------------------------------------------------------
@login_required
def dashboard_encargado(request):
    total_pendientes = OrdenTrabajo.objects.filter(estado="Pendiente").count()
    total_en_proceso = OrdenTrabajo.objects.filter(estado="En Proceso").count()
    total_finalizados = OrdenTrabajo.objects.filter(estado="Finalizado").count()

    from django.utils.timezone import now
    hoy = now().date()
    finalizados_hoy = OrdenTrabajo.objects.filter(
        estado="Finalizado",
        fecha_fin__date=hoy
    ).count()

    return render(request, "operaciones/dashboard_encargado.html", {
        "pendientes": total_pendientes,
        "proceso": total_en_proceso,
        "finalizados": total_finalizados,
        "finalizados_hoy": finalizados_hoy
    })
