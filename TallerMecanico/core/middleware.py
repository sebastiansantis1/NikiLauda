from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

INACTIVIDAD_MAXIMA = 10  # minutos

class UsuarioActivoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ---- RUTAS EXCLUIDAS PARA EVITAR BUCLES ----
        rutas_seguras = [
            reverse("usuario_inactivo"),
            reverse("logout"),
            reverse("login"),
            "/admin/login/",         # LOGIN del Admin
            "/admin/",               # Panel Admin raíz
        ]

        # También excluir cualquier URL que comience con /admin/
        if request.path.startswith("/admin"):
            return self.get_response(request)

        # ---- Validar usuario activo ----
        if request.user.is_authenticated:
            perfil = getattr(request.user, "perfil", None)

            if perfil and not perfil.activo:
                return redirect("usuario_inactivo")

            # Control de inactividad
            ultimo = request.session.get("ultimo_movimiento")
            ahora = timezone.now()

            if ultimo:
                diferencia = ahora - timezone.datetime.fromisoformat(ultimo)

                if diferencia > timedelta(minutes=INACTIVIDAD_MAXIMA):
                    from django.contrib.auth import logout
                    logout(request)
                    return redirect("login")

            request.session["ultimo_movimiento"] = ahora.isoformat()

        return self.get_response(request)



