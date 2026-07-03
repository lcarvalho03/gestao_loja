"""Formulários do app loja.

Validação de CPF/CNPJ via django-localflavor (com dígito verificador) e
máscaras visuais via widgets reutilizáveis (IMask no navegador).
"""

from django import forms
from localflavor.br.forms import BRCNPJField, BRCPFField

from .models import Cliente, Fornecedor, Produto
from .widgets import CelularInput, CNPJInput, CPFCNPJInput, TelefoneInput


class ClienteForm(forms.ModelForm):
    """Formulário de cadastro/edição de cliente com máscaras e validação BR."""

    class Meta:
        """Configuração do ModelForm de Cliente."""

        model = Cliente
        fields = [
            "tipo",
            "nome",
            "documento",
            "email",
            "telefone",
            "celular",
            "endereco",
            "ativo",
        ]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "documento": CPFCNPJInput(),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": TelefoneInput(),
            "celular": CelularInput(),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_documento(self):
        """Valida CPF (PF) ou CNPJ (PJ) conforme o tipo, usando o localflavor."""
        documento = self.cleaned_data.get("documento", "")
        tipo = self.cleaned_data.get("tipo")
        if tipo == Cliente.Tipo.PESSOA_FISICA:
            return BRCPFField().clean(documento)
        return BRCNPJField().clean(documento)


class FornecedorForm(forms.ModelForm):
    """Formulário de cadastro/edição de fornecedor com máscara e validação BR."""

    cnpj = BRCNPJField(label="CNPJ", widget=CNPJInput())

    class Meta:
        """Configuração do ModelForm de Fornecedor."""

        model = Fornecedor
        fields = [
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "email",
            "telefone",
            "celular",
            "endereco",
            "ativo",
        ]
        widgets = {
            "razao_social": forms.TextInput(attrs={"class": "form-control"}),
            "nome_fantasia": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": TelefoneInput(),
            "celular": CelularInput(),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProdutoForm(forms.ModelForm):
    """Formulário de cadastro/edição de produto."""

    class Meta:
        """Configuração do ModelForm de Produto."""

        model = Produto
        fields = [
            "nome",
            "descricao",
            "sku",
            "preco",
            "custo",
            "estoque",
            "categoria",
            "fornecedor",
            "ativo",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "custo": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "estoque": forms.NumberInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "fornecedor": forms.Select(attrs={"class": "form-select"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
