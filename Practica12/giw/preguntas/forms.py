from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput, required=True)
