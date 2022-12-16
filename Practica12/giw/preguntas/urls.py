from django.urls import path

from . import views

app_name = "preguntas"

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
]