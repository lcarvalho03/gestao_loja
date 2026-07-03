"""Exemplo de rotas — cole o conteúdo no core/urls.py do seu projeto."""

from django.contrib import admin
from django.urls import path

from loja import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/novo/", views.cliente_novo, name="cliente_novo"),
    path("fornecedores/novo/", views.fornecedor_novo, name="fornecedor_novo"),
    path("produtos/novo/", views.produto_novo, name="produto_novo"),
]
