from django import forms
from .models import OrdenTrabajo,Vehiculo
from core.validators import validar_solo_texto

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ["cliente", "vehiculo", "descripcion", "zona", "mecanico", "estado", "fecha_inicio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Vehículo parte vacío hasta que el usuario seleccione un cliente
        self.fields['vehiculo'].queryset = Vehiculo.objects.none()

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['vehiculo'].queryset = Vehiculo.objects.filter(cliente_id=cliente_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Caso de edición
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(cliente=self.instance.cliente)
    