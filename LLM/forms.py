from django import forms
from django.core.exceptions import ValidationError
import os

class SubirPDFForm(forms.Form):
    titulo = forms.CharField(max_length=100, required=True)
    archivo = forms.FileField(required=True)
    
    def clean_archivo(self):
        f = self.cleaned_data['archivo']
        tamaño = 25
        extensiones = ('.pdf', '.txt')
        
        # Validar extension
        extension = os.path.splitext(f.name)[1].lower()
        if extension not in extensiones:
            raise ValidationError(f'Solo se permiten archivos {[extension for extension in extensiones]}')
        
        # Validar tamaño
        if f.size > tamaño * 1024 * 1024:
            raise ValidationError(f'El archivo no puede superar el maximo de {tamaño} MB')
        
        return f