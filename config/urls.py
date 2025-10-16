from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')), # inclui as rotas do app
    path('clientes', include('clientes.urls')), # inclui as rotas do clientes
]
