""" Configurações do app core: movimentação de produtos, vendas e relatórios."""
from django.apps import AppConfig

class CoreConfig(AppConfig):
    """ Configurações do aplicativo core: movimentação de produtos, vendas e relatórios."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = "2.0 - MOVIMENTAÇÃO"  # <-- Nome que aparecerá no painel
