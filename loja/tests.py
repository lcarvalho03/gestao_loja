""" Arquivo de testes para o app 'loja' """
from decimal import Decimal
from django.test import TestCase
# from django.utils import timezone
from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque

class MovimentacaoEstoqueSignalsTestCase(TestCase):
    """ Testa os sinais que atualizam o custo do Produto com base nas movimentações de estoque."""
    def setUp(self):
        """Prepara o ambiente de teste antes de rodar os métodos."""
        # 1. Cria uma Categoria obrigatória
        self.categoria = Categoria.objects.create(
            nome="Peças Automotivas",
            descricao="Filtros, óleos e amortecedores"
        )

        # 2. Cria um Fornecedor
        self.fornecedor = Fornecedor.objects.create(
            razao_social="Distribuidora de Componentes SA",
            nome_fantasia="Auto Peças Central",
            cnpj="12345678000190",
            email="contato@autofone.com"
        )

        # 3. Cria um Produto com preço de custo inicial zerado (padrão)
        self.produto = Produto.objects.create(
            nome="Filtro de Óleo PSL74",
            sku="FO-PSL74",
            preco=Decimal("45.00"),
            custo=Decimal("0.00"),  # Começa zerado
            categoria=self.categoria,
            fornecedor=self.fornecedor
        )

    def test_atualizacao_custo_produto_na_entrada_por_compra(self):
        """Garante que salvar uma ENTRADA de COMPRA altera o custo do Produto."""
        novo_preco_custo = Decimal("22.50")

        # Cria a movimentação de estoque simulando uma compra de fornecedor
        MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo=MovimentacaoEstoque.Tipo.ENTRADA,
            origem=MovimentacaoEstoque.Origem.COMPRA,
            quantidade=10,
            valor_unitario=novo_preco_custo,
            fornecedor=self.fornecedor
        )

        # Recarrega o produto do banco de dados para pegar o valor atualizado pelo signal
        self.produto.refresh_from_db()

        # O custo do produto DEVE ser o valor_unitario da movimentação
        self.assertEqual(self.produto.custo, novo_preco_custo)

    def test_nao_altera_custo_produto_se_for_saida(self):
        """Garante que uma movimentação de SAÍDA (venda) NÃO altera o custo do produto."""
        self.produto.custo = Decimal("15.00")
        self.produto.save()

        # Cria uma movimentação de SAÍDA por VENDA
        MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo=MovimentacaoEstoque.Tipo.SAIDA,
            origem=MovimentacaoEstoque.Origem.VENDA,
            quantidade=2,
            valor_unitario=Decimal("45.00")
        )

        self.produto.refresh_from_db()

        # O custo deve permanecer intacto (15.00), e não virar 45.00
        self.assertEqual(self.produto.custo, Decimal("15.00"))

    def test_nao_altera_custo_produto_se_for_ajuste_manual(self):
        """Garante que ENTRADA por AJUSTE MANUAL não altera o preço de custo do produto."""
        self.produto.custo = Decimal("18.00")
        self.produto.save()

        # Cria uma movimentação de entrada, mas com motivo de AJUSTE
        MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo=MovimentacaoEstoque.Tipo.ENTRADA,
            origem=MovimentacaoEstoque.Origem.AJUSTE,
            quantidade=5,
            valor_unitario=Decimal("30.00")
        )

        self.produto.refresh_from_db()

        # O custo deve permanecer intacto (18.00)
        self.assertEqual(self.produto.custo, Decimal("18.00"))
