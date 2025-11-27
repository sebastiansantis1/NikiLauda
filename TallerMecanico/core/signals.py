from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):

    grupos = {
        "ADMINISTRATIVOS": [],
        "ENCARGADOS": [],
        "MECANICOS": [],
        "CLIENTES": []
    }

    for nombre_grupo in grupos:
        grupo, creado = Group.objects.get_or_create(name=nombre_grupo)

        if creado:
            print(f"Grupo creado: {nombre_grupo}")
