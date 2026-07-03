"""Configurações do painel administrativo para o aplicativo loja."""

from django.contrib import admin
from .models import (
    Categoria, Fornecedor, Cliente, Produto,
)

# ==============================================================================
# 1. BLOCO: CADASTROS (Ficam vinculados ao aplicativo 'loja')
# ==============================================================================

# Registro simples apenas para Categoria
admin.site.register(Categoria)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Configurações de exibição do modelo Cliente."""
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """Configurações de exibição do modelo Fornecedor."""
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'ativo')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """Configurações de exibição do modelo Produto."""
    list_display = ('nome',)
    search_fields = ('nome',)
