from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("operaciones/", include("operaciones.urls")),
    path("", include("core.urls")),
]