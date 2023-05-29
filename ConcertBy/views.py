from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Concierto, Artista, Persona, Pago, Ticket
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from django.http import JsonResponse
from django.utils import timezone
# Create your views here.

class MainView(TemplateView):
    template_name = "main.html"

def listadoTickets(request):
    user_id = request.user.id
    persona = obtener_persona(user_id)
    id_persona = persona.id
    tickets = obtener_tickets(id_persona)
    return render(request,'ver_tickets.html', {'tickets':tickets})


def getListadoConcert(request):
    conciertos = Concierto.objects.all()
    nombre_conciertos = []
    for concierto in conciertos:
        nombre_conciertos.append((concierto.id,concierto.nombre, concierto.url_img_concierto))
    return render(request, 'conciertos.html',{'conciertos': nombre_conciertos})

def getInfoConciertoById(request, id_concierto):
    concierto = Concierto.objects.get(id=id_concierto)
    artista = Artista.objects.get(id=concierto.artista_id)
    detalleArtista = {
        'id_artista': artista.id,
        'nombre_artista': artista.nombre,
        'descripcion_artista':  artista.descripcion
    }
    print(type(concierto.fecha_concierto))
    #horarios = Horario.objects.filter(concierto_id= concierto.id)
    return render(request, 'concierto.html', {'nombre_concierto': concierto.nombre,
                                              'des_concierto': concierto.descripcion, 
                                              'url_img_concierto': concierto.url_img_concierto,
                                              'fecha_concierto': concierto.fecha_concierto,
                                              'cantidad_disponible': concierto.cantidad_boletos,
                                              'precio_entradas': concierto.precio,
                                              'id_concierto': id_concierto,
                                              'ubicacion':concierto.ubicacion,
                                              'artista': detalleArtista})

def registro_request(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        validar = form.is_valid()
        if validar:
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
                  context={'registro_form': form,'messages': messages.get_messages(request)})

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
    print(form)
    return render(request=request,
                    template_name='login.html',
                    context={'login_form': form})

def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesión")
    return redirect('login')

def gestionar_pago(request):
    if(request.method == "POST"):

        cantidad_boletos = request.POST.get('cantidadBoletos')
        id_concierto = request.POST.get('id_concierto')
        id_usuario = request.POST.get('id_usuario')
        persona = obtener_persona(id_usuario)
        id_persona = persona.id
        concierto = obtener_concierto(id_concierto)
        fechaPago = timezone.now()
        if(concierto.cantidad_boletos>0):
            if(concierto.cantidad_boletos>int(cantidad_boletos)):
                
                new_ticket = generarTicket(cantidad_boletos,True,id_concierto,id_persona)
                id_new_ticket = new_ticket.id
                totalPago = calcularPago(cantidad_boletos,id_concierto)
                pagarConcierto(fechaPago,totalPago,id_new_ticket)
                

                actualizar_cantBoletosConcierto(cantidad_boletos,concierto)
                response = '¡Compra exitosa!, ha comprado '+cantidad_boletos+' boletos'
                return JsonResponse({'message': response})
            else:
                return JsonResponse({'error': 'Excede el número de boletos disponibles'})
        else:
            return JsonResponse({'error': 'Concierto agotado'})
        
def getInfoTicketById(request):
    id_ticket = request.POST.get('id_ticket')
    id_ticket = int(id_ticket)
    user_id = request.user.id
    persona = obtener_persona(user_id)
    id_persona = persona.id
    ticket = obtener_ticket(id_ticket)
    concierto = obtener_concierto(ticket.concierto_id)
    #validacion de 2 dias de diferencia
    fecha_compra = ticket.fecha_creacion
    fecha_concierto = concierto.fecha_concierto
    diferencia = fecha_concierto-fecha_compra
    if diferencia.days >2:

        # cambiar el ticket a estado 0
        ticket.cancelarTickets = False
        ticket.save()

        # el pago tambien minizar 
        pago = obtener_pago_ticket(id_ticket)
        pago.total-=concierto.precio
        pago.save()
        
        # actualizar la cantidad de boletos
        concierto.cantidad_boletos+=1
        concierto.save()

        response = "Ha cancelado con exito su ticket!"
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'error': 'Usted ya no puede cancelar la compra porque queda menos de dos dias'})

#Funciones de Backend
def obtener_persona(id_user):
    persona = Persona.objects.filter(user_id=id_user).first()
    return persona
def calcularPago(cantidadBoletos, id_concierto):
    concierto = obtener_concierto(id_concierto)
    totalPago = int(cantidadBoletos)*int(concierto.precio)
    return totalPago
def obtener_concierto(id_concierto):
    concierto = Concierto.objects.get(id=id_concierto)
    return concierto
def actualizar_cantBoletosConcierto(cantidad_boletos,concierto):
    concierto.cantidad_boletos -=int(cantidad_boletos)
    concierto.save()
def pagarConcierto(fecha,total,ticket_id):
    pago = Pago(fecha=fecha,total=total,ticket_id=ticket_id)
    pago.save()
def generarTicket(boletos,cancelarTickets,concierto_id,persona_id):
    new_ticket = Ticket(boletos=int(boletos),
                                cancelarTickets=cancelarTickets,
                                concierto_id=int(concierto_id),
                                persona_id=int(persona_id))
    new_ticket.save()
    return new_ticket
def obtener_tickets(id_persona):
    
    resultados = Ticket.objects.filter(persona_id=id_persona,cancelarTickets=1).values(
        'id',
        'concierto__nombre',
        'concierto__fecha_concierto',
        'concierto__ubicacion',
        'concierto__artista__nombre'
    )
    ticketsList = []
    for ticket in resultados:
        print(ticket)
        # ticketsList.append((ticket.id,ticket.nombre, ticket.url_img_concierto))
        ticketsList.append((ticket['id'], 
                            ticket['concierto__nombre'], 
                            ticket['concierto__fecha_concierto'], 
                            ticket['concierto__ubicacion'],
                            ticket['concierto__artista__nombre']))
        
    return ticketsList
def obtener_ticket(id_ticket):
    ticket = Ticket.objects.get(id=id_ticket)
    return ticket
def obtener_pago_ticket(id_ticket):
    pago = Pago.objects.get(ticket_id=id_ticket)
    return pago