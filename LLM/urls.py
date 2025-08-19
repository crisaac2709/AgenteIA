from django.urls import path
from .views import Home, subir_pdf_ajax, UploadPDF

app_name = 'LLM'

urlpatterns = [
    path('', Home, name='Home'),
    path('upload/', UploadPDF, name='upload'),
    path('subir_pdf_ajax', subir_pdf_ajax, name='subir_pdf_ajax'),
]