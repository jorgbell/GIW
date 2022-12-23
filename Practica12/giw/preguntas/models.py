from django.conf import settings
from django.db import models
from django.utils.html import escape

# Create your models here.

class Pregunta(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=250)
    texto = models.CharField(max_length=5000)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def getRespuestas(self):
        return Respuesta.objects.filter(pregunta=self)


    def nRespuestas(self):
        return len(self.getRespuestas())


    def clean(self):
        self.titulo = escape(self.titulo)
        self.texto = escape(self.texto)

    def __str__(self):
        return f'PREGUNTA(id: {self.id}, titulo: {self.titulo}, texto: {self.texto}, fecha: {self.fecha}, autor: {self.autor})'


class Respuesta(models.Model):
    id = models.BigAutoField(primary_key=True)
    texto = models.CharField(max_length=5000)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def clean(self):
        self.texto = escape(self.texto)

    def __str__(self):
        return f'RESPUESTA(id: {self.id}, texto: {self.texto}, fecha: {self.fecha}, autor: {self.autor}, pregunta: {self.pregunta.id})'