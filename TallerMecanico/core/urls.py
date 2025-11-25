from django.urls import path
from . import views

urlpatterns=[
    
    path("",views.home,name="home"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path('usuario-inactivo/', views.usuario_inactivo, name='usuario_inactivo'),
    path("usuarios/", views.gestionar_usuarios, name="gestionar_usuarios"),
    path("usuarios/cambiar-estado/<int:pk>/", views.cambiar_estado_usuario, name="cambiar_estado_usuario"),
    path("usuarios/cambiar-rol/<int:pk>/", views.cambiar_rol_usuario, name="cambiar_rol_usuario"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/detalle/<int:pk>/", views.detalle_usuario, name="detalle_usuario"),

]