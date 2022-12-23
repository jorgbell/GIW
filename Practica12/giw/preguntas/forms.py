from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput, required=True)


class PreguntaForm(forms.Form):
    titulo = forms.CharField(label='Título', max_length=250, required=True)
    texto = forms.CharField(label='Texto', max_length=5000, widget=forms.Textarea)

    
class RespuestaForm(forms.Form):
    texto = forms.CharField(label='Responder', max_length=5000, widget=forms.Textarea)