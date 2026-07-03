""" URLs do app loja: cadastro de clientes, fornecedores e produtos."""
from django.urls import path
from . import views

urlpatterns = [
    # 1. Página inicial (Dashboard com os totais) ao acessar http://127.0.0
    path('', views.home, name='home'),

    # 2. Tela de consulta/listagem de clientes
    path('clientes/', views.clientes, name='clientes'),

    # 3. Telas de inserção de novos cadastros
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('fornecedores/novo/', views.fornecedor_novo, name='fornecedor_novo'),
    path('produtos/novo/', views.produto_novo, name='produto_novo'),
]
