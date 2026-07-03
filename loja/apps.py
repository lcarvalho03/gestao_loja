""" Configurações do app loja: cadastro de clientes, fornecedores e produtos."""
import importlib
from django.apps import AppConfig

class LojaConfig(AppConfig):
    """ Configurações do aplicativo loja: cadastro de clientes, fornecedores e produtos."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loja'
    verbose_name = "1.0 - CADASTROS"  # <-- Nome que aparecerá no painel

    def ready(self):
        # Importa os sinais para garantir que os decorators sejam registrados
        # import loja.signals # type: ignore
        importlib.import_module('loja.signals')
