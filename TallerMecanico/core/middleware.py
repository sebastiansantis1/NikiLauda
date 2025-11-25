from django.shortcuts import redirect
from django.urls import reverse

class UsuarioActivoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ---- RUTAS EXCLUIDAS PARA EVITAR BUCLES ----
        rutas_seguras = [
            reverse("usuario_inactivo"),
            reverse("logout"),
            reverse("login"),
        ]

        # Si la ruta está en las rutas seguras → permitir
        if request.path in rutas_seguras:
            return self.get_response(request)

        # ---- Validar usuario activo ----
        if request.user.is_authenticated:
            perfil = getattr(request.user, "perfil", None)

            # Si tiene perfil y está inactivo → bloquear
            if perfil and not perfil.activo:
                return redirect("usuario_inactivo")

        return self.get_response(request)


