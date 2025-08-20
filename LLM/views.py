from django.shortcuts import render, redirect
from .forms import SubirPDFForm
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
import datetime, os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils import extraerTextoDePDF, cargarDocumentosEnBaseDeConocimiento
from .utils import obtenerLlm, obtenerLlmEmbedding
from pathlib import Path


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
        #subcarpeta = f'documentos/{hoy.year}/{hoy.month:02d}/'
        
        # Nombre de carpeta amigable y unico
        base = slugify(titulo) or 'document'
        ext = os.path.splitext(archivo.name)[1].lower()
        if ext == '.pdf':
            subcarpeta = f'{request.user.username}/documentos/pdf/'
        else:
            subcarpeta = f'{request.user.username}/documentos/txt/'
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
        
        
def kb(request):
    return render(request, 'kb.html')


@require_POST
def crearColeccion(request):
    from .utils import crearBaseDeConocimiento
    try:
        ruta = f'BaseConocimiento/{request.user.username}'
        coleccion = (request.POST.get('coleccion') or "").strip()
        if not coleccion:
            return JsonResponse({
                "ok":False, 
                "error": "Falta nombre de coleccion",
            }, status=400)
        # Creamos la base de conocimiento
        crearBaseDeConocimiento(ruta, coleccion)
        return JsonResponse({
            'ok':True, 
            'respuesta': 'Se creo la base de conocimiento', 
            'coleccion': coleccion
        })
    except Exception as e:
        return JsonResponse({'ok':False, 'errors':str(e)}, status=500)
    

@require_POST
def guardarContexto(request):
    try:
        contexto = (request.POST.get('contexto') or "").strip()
        if not contexto:
            return JsonResponse({
                'ok': False,
                'error': 'Falta contexto'
            }, status=400)
        print(contexto)
        return JsonResponse({
            'ok': True,
            'respuesta': 'Contexto Guardado',
            'contexto': contexto 
        })
    except Exception as e:
        return JsonResponse({'ok':False, 'errors':str(e)}, status=500)
    
    
@require_POST
def llenar_base_conocimiento(request):
    llm_embedding = obtenerLlmEmbedding()
    username = request.user.username

    # Usa Path en TODO y NO reutilices la variable base
    pdf_dir = Path("media") / username / "documentos" / "pdf"
    txt_dir = Path("media") / username / "documentos" / "txt" / "extracciones"
    kb_dir  = Path("BaseConocimiento") / username

    # Asegura carpetas
    txt_dir.mkdir(parents=True, exist_ok=True)
    kb_dir.mkdir(parents=True, exist_ok=True)

    coleccion = (request.POST.get('coleccion') or "").strip()
    if not coleccion:
        return JsonResponse({'ok': False, 'errors': 'Falta coleccion'}, status=400)
    if llm_embedding is None:
        return JsonResponse({'ok': False, 'errors': 'Embeddings no inicializados'}, status=500)
    if not pdf_dir.exists():
        return JsonResponse({'ok': False, 'errors': f'No existe carpeta de PDFs: {pdf_dir}'}, status=400)

    rutas_txt = []
    # Solo procesa PDFs
    for pdf_path in pdf_dir.glob("*.pdf"):
        # NO pisar txt_dir: crea una variable NUEVA por archivo
        txt_path = txt_dir / (pdf_path.stem.lower() + ".txt")
        # DEBUG opcional
        # print("PDF:", pdf_path)
        # print("TXT:", txt_path)
        extraerTextoDePDF(str(pdf_path), str(txt_path))
        rutas_txt.append(str(txt_path))

    if not rutas_txt:
        return JsonResponse({'ok': False, 'errors': 'No se encontraron PDFs'}, status=400)

    cargarDocumentosEnBaseDeConocimiento(
        rutas_txt,
        str(kb_dir),
        coleccion,
        llm_embedding
    )
    return JsonResponse({'ok': True, 'respuesta': 'Datos cargados en base de conocimiento'})
        