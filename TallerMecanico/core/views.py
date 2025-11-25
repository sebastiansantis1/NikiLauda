from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from core.models import PerfilUsuario
from core.validators import validar_rut_chileno


USUARIO_PROTEGIDO = "root"   # Usuario que NO se puede desactivar ni editar


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
def home(request):
    return render(request, "core/home.html")


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm(request)

    return render(request, "core/login.html", {"form": form})


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("home")


# ---------------------------------------------------------
# USUARIO INACTIVO
# ---------------------------------------------------------
def usuario_inactivo(request):
    return render(request, "core/usuario_inactivo.html")


# ---------------------------------------------------------
# PANEL DE USUARIOS (solo ADMIN)
# ---------------------------------------------------------
@login_required
def gestionar_usuarios(request):
    perfil = request.user.perfil

    if perfil.rol != "ADMIN":
        return redirect("usuario_inactivo")

    usuarios = PerfilUsuario.objects.select_related("user").all()

    total_usuarios = usuarios.count()
    usuarios_activos = usuarios.filter(activo=True).count()
    usuarios_inactivos = usuarios.filter(activo=False).count()

    return render(request, "core/gestionar_usuarios.html", {
        "usuarios": usuarios,
        "total_usuarios": total_usuarios,
        "usuarios_activos": usuarios_activos,
        "usuarios_inactivos": usuarios_inactivos,
    })


# ---------------------------------------------------------
# CAMBIAR ESTADO DE USUARIO (activar/desactivar)
# ---------------------------------------------------------
@login_required
def cambiar_estado_usuario(request, pk):
    admin = request.user.perfil

    if admin.rol != "ADMIN":
        return redirect("usuario_inactivo")

    usuario = get_object_or_404(PerfilUsuario, pk=pk)

    # ❌ PROTECCIÓN TOTAL DEL USUARIO ROOT
    if usuario.user.username == USUARIO_PROTEGIDO:
        return redirect("gestionar_usuarios")

    usuario.activo = not usuario.activo
    usuario.save()

    return redirect("gestionar_usuarios")


# ---------------------------------------------------------
# CAMBIAR ROL
# ---------------------------------------------------------
@login_required
def cambiar_rol_usuario(request, pk):
    admin = request.user.perfil

    if admin.rol != "ADMIN":
        return redirect("usuario_inactivo")

    usuario = get_object_or_404(PerfilUsuario, pk=pk)

    # ❌ Nadie puede cambiar el rol del usuario root
    if usuario.user.username == USUARIO_PROTEGIDO:
        return render(request, "core/cambiar_rol.html", {
            "usuario": usuario,
            "error": "El usuario root está protegido y no puede cambiar su rol."
        })

    if request.method == "POST":
        nuevo_rol = request.POST.get("rol")

        # ❌ No puedes cambiar tu propio rol
        if usuario == admin:
            return render(request, "core/cambiar_rol.html", {
                "usuario": usuario,
                "error": "No puedes cambiar tu propio rol."
            })

        usuario.rol = nuevo_rol
        usuario.save()

        return redirect("gestionar_usuarios")

    return render(request, "core/cambiar_rol.html", {"usuario": usuario})


# ---------------------------------------------------------
# CREAR USUARIO NUEVO
# ---------------------------------------------------------
@login_required
def crear_usuario(request):
    admin = request.user.perfil

    if admin.rol != "ADMIN":
        return redirect("usuario_inactivo")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        rut = request.POST.get("rut")
        rol = request.POST.get("rol")

        errors = []

        if not username:
            errors.append("El nombre de usuario es obligatorio.")
        if not password:
            errors.append("La contraseña es obligatoria.")
        if not rut:
            errors.append("El RUT es obligatorio.")

        from django.contrib.auth.models import User
        from core.models import PerfilUsuario
        from django.core.exceptions import ValidationError

        # Validar rut real (tu función)
        try:
            rut_normalizado = validar_rut_chileno(rut)
        except ValidationError as e:
            errors.append(str(e))

        # Validar duplicados
        if User.objects.filter(username=username).exists():
            errors.append("El usuario ya existe.")
        if PerfilUsuario.objects.filter(rut=rut_normalizado).exists():
            errors.append("El RUT ya está registrado.")

        if errors:
            return render(request, "core/crear_usuario.html", {"errors": errors})

        # Crear usuario (NO crea perfil porque eliminamos la señal)
        user = User.objects.create_user(username=username, password=password)

        # Crear perfil correctamente
        PerfilUsuario.objects.create(
            user=user,
            rut=rut_normalizado,
            rol=rol,
            activo=True
        )

        return redirect("gestionar_usuarios")

    return render(request, "core/crear_usuario.html")


# ---------------------------------------------------------
# DETALLE DE USUARIO
# ---------------------------------------------------------
@login_required
def detalle_usuario(request, pk):
    admin = request.user.perfil

    if admin.rol != "ADMIN":
        return redirect("usuario_inactivo")

    usuario = get_object_or_404(PerfilUsuario, pk=pk)

    # Mostrar trabajos asignados si es mecánico
    trabajos = None
    if usuario.rol == "MECANICO":
        from operaciones.models import OrdenTrabajo
        trabajos = OrdenTrabajo.objects.filter(mecanico=usuario)

    return render(request, "core/detalle_usuario.html", {
        "usuario": usuario,
        "trabajos": trabajos
    })
