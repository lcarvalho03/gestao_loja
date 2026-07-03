"""Views do app loja: cadastro de clientes, fornecedores e produtos."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm, FornecedorForm, ProdutoForm
from .models import Cliente, Fornecedor, Produto


@login_required
def home(request):
    """Página inicial: dashboard com totais e atalhos para os cadastros."""
    contexto = {
        "total_clientes": Cliente.objects.count(),
        "total_fornecedores": Fornecedor.objects.count(),
        "total_produtos": Produto.objects.count(),
    }
    return render(request, "loja/home.html", contexto)


@login_required
def clientes(request):
    """Exibe a lista de clientes cadastrados."""
    lista_de_clientes = Cliente.objects.all()
    return render(request, "loja/clientes.html", {"clientes": lista_de_clientes})


@login_required
def cliente_novo(request):
    """Exibe e processa o formulário de cadastro de cliente."""
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente cadastrado com sucesso.")
            return redirect("cliente_novo")
    else:
        form = ClienteForm()
    return render(request, "loja/form.html", {"form": form, "titulo": "Novo cliente"})


@login_required
def fornecedor_novo(request):
    """Exibe e processa o formulário de cadastro de fornecedor."""
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fornecedor cadastrado com sucesso.")
            return redirect("fornecedor_novo")
    else:
        form = FornecedorForm()
    return render(
        request, "loja/form.html", {"form": form, "titulo": "Novo fornecedor"}
    )


@login_required
def produto_novo(request):
    """Exibe e processa o formulário de cadastro de produto."""
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect("produto_novo")
    else:
        form = ProdutoForm()
    return render(request, "loja/form.html", {"form": form, "titulo": "Novo produto"})
