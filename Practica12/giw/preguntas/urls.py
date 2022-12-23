from django.urls import path

from . import views

app_name = "preguntas"

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutFunction, name='logout'),
    path('login', views.loginFunction, name='login'),
    path('<int:N>', views.preguntaN, name='preguntaN'),
]