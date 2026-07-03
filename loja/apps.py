""" Configurações do app loja: cadastro de clientes, fornecedores e produtos."""
from django.apps import AppConfig

class LojaConfig(AppConfig):
    """ Configurações do aplicativo loja: cadastro de clientes, fornecedores e produtos."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loja'
    verbose_name = "1.0 - CADASTROS"  # <-- Nome que aparecerá no painel
