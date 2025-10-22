from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('novo/', views.novo_produto, name='novo_produto'),
    path('<int:id>/', views.atualizar_produto, name='atualizar_produto'),
    path('<int:id>/delete/', views.deletar_produto, name='deletar_produto'),
]