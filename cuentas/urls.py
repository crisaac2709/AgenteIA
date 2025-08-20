from django.urls import path
from .views import registro, loginView, api_registro, logoutView

app_name = 'cuentas'

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', loginView, name='login'),
    path('api_registro', api_registro, name='api_registro'),
    path('logout', logoutView, name='logout'),
]