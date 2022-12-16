from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

# Create your views here.

def index(request):
    return render(request, 'preguntas/index.html')

def login(request):
    form = LoginForm()
    return render(request, 'preguntas/login.html', {'login_form':form})

def logout(request):
    return HttpResponse("pagina de logout")