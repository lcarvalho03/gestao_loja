"""Modelos de dados do sistema de loja: clientes, fornecedores, produtos,
faturas/cotações e movimentações de estoque."""

from decimal import Decimal

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.br.models import BRCPFField, BRCNPJField

# Alíquota de imposto aplicada às faturas/cotações (16%).
TAXA_IMPOSTO = Decimal("0.16")


class Categoria(models.Model):
    """Categoria usada para agrupar produtos."""

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        """Metadados e ordenação padrão da categoria."""

        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        """Retorna o nome da categoria."""
        return str(self.nome)


class Fornecedor(models.Model):
    """Fornecedor que abastece os produtos da loja."""

    razao_social = models.CharField("Razão social", max_length=200)
    nome_fantasia = models.CharField("Nome fantasia", max_length=200, blank=True)
    cnpj = BRCNPJField("CNPJ", max_length=18, unique=True)
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField("Telefone", region="BR", blank=True)
    celular = PhoneNumberField("Celular", region="BR", blank=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadados e ordenação padrão do fornecedor."""

        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["razao_social"]

    def __str__(self):
        """Retorna o nome fantasia ou, na ausência, a razão social."""
        return str(self.nome_fantasia or self.razao_social)


class Cliente(models.Model):
    """Cliente (pessoa física ou jurídica) que adquire produtos."""

    class Tipo(models.TextChoices):
        """Tipos de cliente aceitos."""

        PESSOA_FISICA = "PF", "Pessoa física"
        PESSOA_JURIDICA = "PJ", "Pessoa jurídica"

    tipo = models.CharField(max_length=2, choices=Tipo.choices, default=Tipo.PESSOA_JURIDICA)
    # Para PJ usa-se a razão social; para PF, o nome completo.
    nome = models.CharField("Nome / Razão social", max_length=200)
    documento = BRCPFField("CPF / CNPJ", max_length=14, unique=True)
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField("Telefone", region="BR", blank=True)
    celular = PhoneNumberField("Celular", region="BR", blank=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadados e ordenação padrão do cliente."""

        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        """Retorna o nome/razão social do cliente."""
        return str(self.nome)


class Produto(models.Model):
    """Produto comercializado pela loja."""

    nome = models.CharField(max_length=150)
    descricao = models.TextField("Descrição", blank=True)
    sku = models.CharField("SKU", max_length=50, unique=True)
    preco = models.DecimalField("Preço de venda", max_digits=10, decimal_places=2)
    custo = models.DecimalField(
        "Preço de custo", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    estoque = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name="produtos",
        null=True,
        blank=True,
    )
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadados e ordenação padrão do produto."""

        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        """Retorna o nome do produto."""
        return str(self.nome)


class Documento(models.Model):
    """Fatura ou cotação emitida para um cliente/empresa compradora."""

    class Tipo(models.TextChoices):
        """Distingue uma fatura de uma cotação."""

        FATURA = "FATURA", "Fatura"
        COTACAO = "COTACAO", "Cotação"

    class Status(models.TextChoices):
        """Estados possíveis do documento."""

        RASCUNHO = "RASCUNHO", "Rascunho"
        EMITIDO = "EMITIDO", "Emitido"
        PAGO = "PAGO", "Pago"
        CANCELADO = "CANCELADO", "Cancelado"

    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.FATURA)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.RASCUNHO
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="documentos",
    )
    produtos = models.ManyToManyField(
        Produto,
        through="ItemDocumento",
        related_name="documentos",
    )
    taxa_imposto = models.DecimalField(
        "Alíquota de imposto",
        max_digits=5,
        decimal_places=4,
        default=TAXA_IMPOSTO,
        help_text="Fração aplicada sobre o subtotal (ex.: 0.16 = 16%).",
    )
    observacoes = models.TextField("Observações", blank=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_validade = models.DateField(null=True, blank=True)

    class Meta:
        """Metadados e ordenação padrão do documento."""

        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-data_emissao"]
        app_label = 'core'


    def __str__(self):
        """Retorna o tipo, o número e o cliente do documento."""
        return f"{self.get_tipo_display()} #{self.pk} - {self.cliente.nome}"

    @property
    def subtotal(self):
        """Soma dos subtotais dos itens, antes do imposto."""
        return sum(
            (item.subtotal for item in self.itens.all()), Decimal("0.00")
        )

    @property
    def valor_imposto(self):
        """Valor do imposto aplicado sobre o subtotal."""
        return (self.subtotal * self.taxa_imposto).quantize(Decimal("0.01"))

    @property
    def total(self):
        """Total do documento (subtotal + imposto)."""
        return self.subtotal + self.valor_imposto


class ItemDocumento(models.Model):
    """Item (linha) de um documento, ligando produto e documento."""

    documento = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        related_name="itens",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_documento",
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(
        "Preço unitário", max_digits=10, decimal_places=2
    )

    class Meta:
        """Metadados e restrição de unicidade do item."""

        verbose_name = "Item do documento"
        verbose_name_plural = "Itens do documento"
        unique_together = ("documento", "produto")
        app_label = 'core'

    def __str__(self):
        """Retorna a quantidade e o nome do produto do item."""
        return f"{self.quantidade}x {self.produto.nome}"

    @property
    def subtotal(self):
        """Subtotal da linha (quantidade x preço unitário)."""
        return self.quantidade * self.preco_unitario


class MovimentacaoEstoque(models.Model):
    """Entradas e saídas de estoque — base para os relatórios."""

    class Tipo(models.TextChoices):
        """Sentido da movimentação de estoque."""

        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    class Origem(models.TextChoices):
        """Motivo que gerou a movimentação."""

        COMPRA = "COMPRA", "Compra de fornecedor"
        VENDA = "VENDA", "Venda"
        AJUSTE = "AJUSTE", "Ajuste manual"
        DEVOLUCAO = "DEVOLUCAO", "Devolução"

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="movimentacoes",
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    origem = models.CharField(
        max_length=10, choices=Origem.choices, default=Origem.AJUSTE
    )
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(
        "Valor unitário", max_digits=10, decimal_places=2
    )
    # Vincula a saída/venda ao documento (fatura) que a originou, quando houver.
    documento = models.ForeignKey(
        Documento,
        on_delete=models.SET_NULL,
        related_name="movimentacoes",
        null=True,
        blank=True,
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        related_name="movimentacoes",
        null=True,
        blank=True,
    )
    observacoes = models.TextField("Observações", blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadados e ordenação padrão da movimentação."""

        verbose_name = "Movimentação de estoque"
        verbose_name_plural = "Movimentações de estoque"
        ordering = ["-data"]
        app_label = 'core'

    def __str__(self):
        """Retorna o tipo, a quantidade e o produto da movimentação."""
        return f"{self.get_tipo_display()} - {self.quantidade}x {self.produto.nome}"

    @property
    def valor_total(self):
        """Valor total da movimentação (quantidade x valor unitário)."""
        return self.quantidade * self.valor_unitario
