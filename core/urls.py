""" URLs do projeto Django. Redireciona a página inicial para o painel de administração seguro. """
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect  # <-- CORREÇÃO: O 'redirect' vem de shortcuts!

# Função simples para mandar a página inicial direto para o painel seguro
def redireciona_para_painel(request):
    """ Redireciona a página inicial para o painel de administração seguro do Django."""
    return redirect('admin:index')

urlpatterns = [
    # Ao acessar http://127.0.0, ele joga você direto para o painel com login
    path('', redireciona_para_painel, name='home'),

    # Rota oficial do painel automático do Django
    path('admin/', admin.site.urls),
]

# Configurações oficiais de títulos do Django Admin
admin.site.site_header = "Gestão da Loja"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Áreas do Sistema"
