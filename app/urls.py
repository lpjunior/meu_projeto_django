from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('novo/', views.formulario_produto, name='novo_produto'),
    path('criar/', views.cadastrar_produto, name='cadastrar_produto'),
]