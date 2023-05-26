from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Concierto, Artista, Persona, Pago, Ticket
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistroForm, LoginForm
# Create your views here.

class MainView(TemplateView):
    template_name = "main.html"

def getListadoConcert(request):
    conciertos = Concierto.objects.all()
    nombre_conciertos = []
    for concierto in conciertos:
        nombre_conciertos.append((concierto.id,concierto.nombre, concierto.url_img_concierto))
    return render(request, 'conciertos.html',{'conciertos': nombre_conciertos})

def getInfoConciertoById(request, id_concierto):
    concierto = Concierto.objects.get(id=id_concierto)
    #horarios = Horario.objects.filter(concierto_id= concierto.id)
    return render(request, 'concierto.html', {'nombre_concierto': concierto.nombre,'des_concierto': concierto.descripcion, 'url_img_concierto': concierto.url_img_concierto})

def registro_request(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Se ha registrado exitosamente')
            return redirect('landing')
        else:
            messages.error(request,'Información no válida')
    else:
        form = RegistroForm()
    return render(request=request,
                  template_name='registro.html',
                  context={'registro_form': form})

def login_request(request):
    if request.method == 'POST' :
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f'Ha iniciado sesión como: {username}')
                return redirect('landing')
            messages.error(request, 'Credenciales incorrectas')
        messages.error(request, 'Credenciales incorrectas')
    form = LoginForm()
    return render(request=request,
                    template_name='login.html',
                    context={'login_form': form})
