from django.urls import path
from .views import Home, subir_pdf_ajax, UploadPDF, kb, crearColeccion, guardarContexto, llenar_base_conocimiento, chat, obtener_base_conocimiento, chat_api

app_name = 'LLM'

urlpatterns = [
    path('', Home, name='Home'),
    path('upload/', UploadPDF, name='upload'),
    path('subir_pdf_ajax', subir_pdf_ajax, name='subir_pdf_ajax'),
    path('kb', kb, name='kb'),
    path('crear_coleccion', crearColeccion, name='crear_coleccion'),
    path('guardar_contexto', guardarContexto, name='guardar_contexto'),
    path('cargar_documentos', llenar_base_conocimiento, name='cargar_documentos'),
    path('chat', chat, name='chat'),
    path('obtener_base_conocimiento', obtener_base_conocimiento, name='obtener_base_conocimiento'),
    path('chat_api', chat_api, name='chat_api'),
]