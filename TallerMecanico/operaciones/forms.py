from django import forms
from .models import OrdenTrabajo
from core.validators import validar_solo_texto

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['cliente', 'vehiculo', 'descripcion', 'zona', 'mecanico','estado', 'fecha_inicio', 'fecha_fin']
        
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            })
        }
    
    