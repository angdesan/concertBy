from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ConcertBy.models import Persona
class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length = 60)
    cedula = forms.CharField(max_length=10)
    telefono = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username','nombre','cedula','email','telefono','password1','password2')
    def __init__(self, *args, **kwargs):
        super(RegistroForm,self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'general'
    
    def save(self,commit=True):
        user = super(RegistroForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        # creacion Persona
        c_nombre = self.cleaned_data['nombre']
        c_cedula = self.cleaned_data['cedula']
        c_telefono = self.cleaned_data['telefono']
        if commit:
            user.save()
            new_persona = Persona(nombre=c_nombre,cedula= c_cedula,telefono = c_telefono, user=user)
            new_persona.save()
        return user



