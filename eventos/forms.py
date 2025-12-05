from django import forms
from datetime import date
from django.utils import timezone

from .models import Evento


class FormularioEvento(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombre', 'descripcion', 'fecha', 'hora', 'lugar',
            'capacidad', 'forma_recinto', 'categoria', 'imagen',
            'precio_vip', 'precio_avanzado', 'precio_normal'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Feria de Tecnología',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe brevemente el evento...',
                'required': True
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Auditorio Central',
                'required': True
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej. 300',
                'required': True
            }),
            'forma_recinto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_categoria',
                'required': True
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'precio_vip': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ej. 15000',
                'required': True
            }),
            'precio_avanzado': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ej. 10000',
                'required': True
            }),
            'precio_normal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ej. 5000',
                'required': True
            }),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha del evento no puede ser en el pasado.")
        return fecha

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get("capacidad")
        if capacidad is not None and capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser mayor que cero.")
        return capacidad

    def clean(self):
        cleaned = super().clean()
        vip = cleaned.get("precio_vip")
        avanzado = cleaned.get("precio_avanzado")
        normal = cleaned.get("precio_normal")
        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")
        lugar = cleaned.get("lugar")

        # Validación jerarquía de precios
        if vip and avanzado and normal:
            if vip < avanzado or vip < normal:
                raise forms.ValidationError("El precio VIP debe ser el más alto.")
            if avanzado < normal:
                raise forms.ValidationError("El precio Avanzado debe ser mayor que el Normal.")

        # Validación: no permitir eventos en el mismo lugar, fecha y hora
        if fecha and hora and lugar:
            conflicto = Evento.objects.filter(
                fecha=fecha,
                hora=hora,
                lugar__iexact=lugar
            )
            if self.instance.pk:
                conflicto = conflicto.exclude(pk=self.instance.pk)
            if conflicto.exists():
                raise forms.ValidationError("Ya existe un evento en este lugar, fecha y hora.")

        # Validación extra: si la fecha es hoy, hora futura obligatoria
        if fecha == date.today() and hora:
            ahora = timezone.localtime().time()
            if hora < ahora:
                raise forms.ValidationError("La hora del evento no puede ser anterior a la actual.")

        return cleaned
