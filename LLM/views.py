from django.shortcuts import render, redirect
from .forms import SubirPDFForm
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
import datetime, os
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
def Home(request):
    return render(request, 'Home.html')


def UploadPDF(request):
    return render(request, 'subirPDF.html')

@require_POST
def subir_pdf_ajax(request):
    form = SubirPDFForm(request.POST, request.FILES)
    if form.is_valid():
        titulo = form.cleaned_data['titulo']
        archivo = form.cleaned_data['archivo']
        
        # colocamos la carpeta de destino (media/documentos/AAAA/MM/)
        hoy = datetime.date.today()
        subcarpeta = f'documentos/{hoy.year}/{hoy.month:02d}/'
        
        # Nombre de carpeta amigable y unico
        base = slugify(titulo) or 'document'
        ext = os.path.splitext(archivo.name)[1].lower()
        nombre_archivo = f'{base}-{hoy.strftime("%Y%m%d")}{ext}'
        
        # Guardar
        fs = FileSystemStorage(location='media/' + subcarpeta, base_url='/media/' + subcarpeta)
        nombre_final = fs.save(nombre_archivo, archivo)
        url = fs.url(nombre_final)
        
        return JsonResponse({
            "ok": True,
            "url": url,
            "titulo": titulo
        })
    else:
        return JsonResponse({
            "ok": False,
            "errors": form.errors
        }, status = 400)
            