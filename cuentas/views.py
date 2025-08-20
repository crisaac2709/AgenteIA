from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.urls import reverse

# Create your views here.
def registro(request):
    return render(request, 'registro.html')

@require_POST
def api_registro(request):
    form = CustomUserCreationForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save()
        return JsonResponse({
            'ok': True,
            'url' : reverse('cuentas:login')
        })
    else:
        return JsonResponse({
            'ok': False,
            'errors' : form.errors
        }, status = 400)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('LLM:Home')
    
    return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return redirect('cuentas:login')