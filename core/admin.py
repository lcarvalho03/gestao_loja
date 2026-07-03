"""Configurações do painel administrativo para o aplicativo core (MOVIMENTAÇÕES)."""

from django.contrib import admin
# IMPORTANTE: Buscamos os modelos que nasceram na pasta loja para registrá-los aqui no core!
from loja.models import Documento, ItemDocumento, MovimentacaoEstoque

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    """Registra o modelo Documento dentro do bloco de Movimentações."""
    pass

@admin.register(ItemDocumento)
class ItemDocumentoAdmin(admin.ModelAdmin):
    """Registra o modelo ItemDocumento dentro do bloco de Movimentações."""
    pass

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    """Registra o modelo MovimentacaoEstoque dentro do bloco de Movimentações."""
    pass
