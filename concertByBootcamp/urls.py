"""
URL configuration for concertByBootcamp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ConcertBy import views

urlpatterns = [
    path("", views.MainView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    path("registro", views.registro_request, name='registro'),
    path("login", views.login_request, name='login'),
    path("logout", views.logout_request, name='logout'),
    path("getInfoConciertoById/<int:id_concierto>",views.getInfoConciertoById,name="getInfoConciertoById"),
    path('conciertos/',views.getListadoConcert, name='getListadoConcert'),
    path('gestionar_pago',views.gestionar_pago, name='gestionar_pago')
]
