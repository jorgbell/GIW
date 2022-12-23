from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

from .models import Pregunta, Respuesta

from .forms import LoginForm, PreguntaForm, RespuestaForm

# Create your views here.

@require_http_methods(['GET', 'POST'])
def index(request):

    # Peticiones POST
    if request.method == 'POST':
        return postPregunta(request)

    # Peticiones GET
    preguntas = Pregunta.objects.order_by('-fecha')
    pregForm = PreguntaForm()

    return render(request, 'preguntas/index.html', {'preguntas': preguntas, 'pregunta_form': pregForm})


@login_required(login_url='preguntas:login')
def postPregunta(request):
    form = PreguntaForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    titulo = form.cleaned_data['titulo']
    texto = form.cleaned_data['texto']

    preguna = Pregunta(titulo=titulo, texto=texto, autor=request.user)
    preguna.save()

    return redirect(reverse('preguntas:index'))


# Pedrito, passpedro
# Joselito, passjose
@require_http_methods(['GET', 'POST'])
def loginFunction(request):

    # Peticiones GET
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'preguntas/login.html', {'login_form':form})

    # Peticiones POST
    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Autenticar usuario
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('preguntas:index'))
    else:
        return render(request, 'preguntas/loginError.html')


@require_GET
def logoutFunction(request):
    logout(request)
    return redirect(reverse('preguntas:index'))


@login_required(login_url='preguntas:login')
@require_GET
def preguntaN(request, N):

    # Comprobar que la pregunta N existe
    pregunta = Pregunta.objects.get(pk=N)
    if not pregunta:
        return HttpResponseBadRequest("La pregunta no existe")

    # Peticiones GET
    pregunta = Pregunta.objects.get(pk=N)
    respuestas = pregunta.getRespuestas().order_by('-fecha')
    respuestaForm = RespuestaForm()

    return render(request, 'preguntas/preguntaN.html', {'pregunta':pregunta, 'respuestas':respuestas, 'respuesta_form': respuestaForm})


@login_required(login_url='preguntas:login')
@require_POST
def postRespuesta(request, N):

    # Comprobar que la pregunta N existe
    pregunta = Pregunta.objects.get(pk=N)
    if not pregunta:
        return HttpResponseBadRequest("La pregunta no existe")

    form = RespuestaForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    texto = form.cleaned_data['texto']
    pregunta = Pregunta.objects.get(pk=N)

    respuesta = Respuesta(texto=texto, autor = request.user, pregunta=pregunta)
    respuesta.save()

    return redirect(reverse('preguntas:preguntaN', kwargs={'N':N}))