from django.contrib import admin
from django.urls import path, include
from app.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'), # inclui as rotas do dashboard
    path('admin/', admin.site.urls),
    path('produtos/', include('app.urls')), # inclui as rotas do app
    path('clientes/', include('clientes.urls')), # inclui as rotas do clientes
]
