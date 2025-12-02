from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Importar SOLO dentro del método
        try:
            self.crear_grupos_y_permisos()
        except:
            pass

    def crear_grupos_y_permisos(self):
        # Importar aquí para evitar AppRegistryNotReady
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from operaciones.models import OrdenTrabajo

        grupos = {
            "ADMINISTRATIVOS": ["add_ordentrabajo", "change_ordentrabajo", "view_ordentrabajo", "delete_ordentrabajo"],
            "ENCARGADOS": ["view_ordentrabajo", "change_ordentrabajo"],
            "MECANICOS": ["view_ordentrabajo"],
            "CLIENTES": ["view_ordentrabajo"],
        }

        ct = ContentType.objects.get_for_model(OrdenTrabajo)

        for nombre, permisos in grupos.items():
            grupo, creado = Group.objects.get_or_create(name=nombre)
            grupo.permissions.clear()

            for codename in permisos:
                try:
                    permiso = Permission.objects.get(content_type=ct, codename=codename)
                    grupo.permissions.add(permiso)
                except Permission.DoesNotExist:
                    pass

            grupo.save()

