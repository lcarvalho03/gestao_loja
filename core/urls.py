""" 
    URLs do projeto Django. 
    Redireciona a página inicial para o painel de administração seguro. 
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rota oficial do painel automático do Django
    path('admin/', admin.site.urls),
    
    # Ao acessar http://127.0.0, ele joga você direto para o painel com login
    path('', include('loja.urls')),  # <-- Inclui as URLs do app 'loja' para a página inicial
]

# Configurações oficiais de títulos do Django Admin
admin.site.site_header = "Gestão da Loja"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Áreas do Sistema"
