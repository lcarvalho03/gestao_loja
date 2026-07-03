"""Widgets reutilizáveis com máscara embutida.

A ideia é "definir o tipo do campo" e a máscara vir junto: basta usar
`TelefoneInput`, `CelularInput`, `CPFCNPJInput` ou `CNPJInput` como widget
no formulário. A máscara visual em si é aplicada no navegador (IMask) através
da classe CSS que cada widget injeta — máscara é, por natureza, frontend.

Telefone e celular usam o `RegionalPhoneNumberWidget` do phonenumber-field,
que renderiza o número no formato nacional (ex.: "(11) 99999-8888").
"""

from django import forms
from phonenumber_field.widgets import RegionalPhoneNumberWidget


def _merge_attrs(mask_class, placeholder, attrs):
    """Combina a classe de máscara e o placeholder com os attrs recebidos."""
    final_attrs = {"class": f"form-control {mask_class}".strip()}
    if placeholder:
        final_attrs["placeholder"] = placeholder
    if attrs:
        extra_class = attrs.pop("class", "")
        if extra_class:
            final_attrs["class"] = f"{final_attrs['class']} {extra_class}".strip()
        final_attrs.update(attrs)
    return final_attrs


class _MaskedTextInput(forms.TextInput):
    """Base para inputs de texto com classe de máscara e placeholder padrão."""

    mask_class = ""
    default_placeholder = ""

    def __init__(self, attrs=None):
        """Aplica a classe de máscara e o placeholder do subtipo."""
        super().__init__(_merge_attrs(self.mask_class, self.default_placeholder, attrs))

    def format_value(self, value):
        """Formata o valor vindo do banco de dados para exibição nas telas de Edição."""
        return formatar_documento(value)


class CPFCNPJInput(_MaskedTextInput):
    """Documento dinâmico: CPF até 11 dígitos, CNPJ a partir de 12."""

    mask_class = "mask-documento"
    default_placeholder = "CPF ou CNPJ"


class CNPJInput(_MaskedTextInput):
    """CNPJ: 00.000.000/0000-00."""

    mask_class = "mask-cnpj"
    default_placeholder = "00.000.000/0000-00"


class TelefoneInput(RegionalPhoneNumberWidget):
    """Telefone fixo com máscara (00) 0000-0000 e formato nacional."""

    def __init__(self, attrs=None):
        """Aplica a classe da máscara de telefone e o placeholder."""
        super().__init__(attrs=_merge_attrs("mask-telefone", "(00) 0000-0000", attrs))

class CelularInput(RegionalPhoneNumberWidget):
    """Celular com máscara (00) 00000-0000 e formato nacional."""

    def __init__(self, attrs=None):
        """Aplica a classe da máscara de celular e o placeholder."""
        super().__init__(attrs=_merge_attrs("mask-celular", "(00) 00000-0000", attrs))

def formatar_documento(valor):
    if not valor:
        return ""
    numeros = "".join(filter(str.isdigit, str(valor)))
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    elif len(numeros) == 14:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
    return valor
