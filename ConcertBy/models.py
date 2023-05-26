from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.

class Persona(models.Model):
    user = models.OneToOneField('auth.user',on_delete=models.PROTECT, related_name='user',default=None)
    nombre = models.CharField(max_length=60)
    cedula = models.CharField(max_length=10)
    telefono = models.CharField(max_length=30,null=True, blank=True)

class Concierto(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200)
    fecha_concierto = models.DateTimeField(default=timezone.now)
    cantidad_boletos = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    url_img_concierto = models.CharField(max_length=2083, default="valor predeterminado")
    artista = models.ForeignKey('Artista',on_delete=models.PROTECT, related_name='artista')

class Ticket(models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    boletos = models.IntegerField(default=1)
    cancelarTickets = models.BooleanField(default=False)
    persona = models.ForeignKey('Persona',on_delete=models.PROTECT,related_name='persona')
    concierto = models.ForeignKey('Concierto',on_delete=models.PROTECT,related_name='concierto')

class Pago(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    ticket = models.ForeignKey('Ticket',on_delete=models.PROTECT,related_name='ticket')
    total = models.FloatField()

class Artista(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=300)
    
