from django import forms
from .models import OrdenTrabajo, Vehiculo
from core.models import ZonaTrabajo, PerfilUsuario


class OrdenTrabajoForm(forms.ModelForm):

    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = OrdenTrabajo
        fields = [
            "cliente",
            "vehiculo",
            "descripcion",
            "zona",
            "mecanico",
            "estado",
            "fecha_inicio",
            "fecha_fin",
        ]

        widgets = {
            "descripcion": forms.Textarea(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "vehiculo": forms.Select(attrs={"class": "form-select"}),
            "zona": forms.Select(attrs={"class": "form-select"}),
            "mecanico": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar solamente mecánicos activos y disponibles
        self.fields['mecanico'].queryset = PerfilUsuario.objects.filter(
            rol="MECANICO",
            activo=True
        )

        # Vehículo parte vacío hasta elegir cliente
        self.fields['vehiculo'].queryset = Vehiculo.objects.none()

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['vehiculo'].queryset = Vehiculo.objects.filter(
                    cliente_id=cliente_id
                )
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            # Caso de edición
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(
                cliente=self.instance.cliente
            )

    