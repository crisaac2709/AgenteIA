from django.urls import path
from .views import Home, subir_pdf_ajax, UploadPDF, kb, crearColeccion, guardarContexto, llenar_base_conocimiento

app_name = 'LLM'

urlpatterns = [
    path('', Home, name='Home'),
    path('upload/', UploadPDF, name='upload'),
    path('subir_pdf_ajax', subir_pdf_ajax, name='subir_pdf_ajax'),
    path('kb', kb, name='kb'),
    path('crear_coleccion', crearColeccion, name='crear_coleccion'),
    path('guardar_contexto', guardarContexto, name='guardar_contexto'),
    path('cargar_documentos', llenar_base_conocimiento, name='cargar_documentos'),
]