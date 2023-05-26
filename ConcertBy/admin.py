from django.contrib import admin

# Register your models here.
from .models import Persona,Pago,Ticket,Artista,Concierto
admin.site.register(Persona)
admin.site.register(Pago)
admin.site.register(Artista)
admin.site.register(Ticket)
admin.site.register(Concierto)