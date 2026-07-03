""" Arquivo de sinais do aplicativo 'loja' para atualizar o custo do produto no estoque. """
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovimentacaoEstoque # , Produto

@receiver(post_save, sender=MovimentacaoEstoque)
def atualizar_custo_produto_no_estoque(sender, instance, created, **kwargs):
    """
    Sempre que uma movimentação de estoque for salva, se for uma ENTRADA 
    por motivo de COMPRA, atualiza o preço de custo do produto correspondente.
    """
    # Verifica se é uma entrada de compra e se possui um produto e valor válidos
    if (
        instance.tipo == MovimentacaoEstoque.Tipo.ENTRADA
        and instance.origem == MovimentacaoEstoque.Origem.COMPRA
        and instance.produto
        and instance.valor_unitario is not None
    ):
        produto = instance.produto

        # Atualiza o campo 'custo' da classe Produto com o 'valor_unitario' do movimento
        produto.custo = instance.valor_unitario
        produto.estoque += instance.quantidade  # Atualiza o estoque do produto
        produto.fornecedor = instance.fornecedor# Mantém o fornecedor do produto

        # Salva apenas os campos 'custo' e 'estoque' por performance e para evitar colisões
        produto.save(update_fields=['custo', 'estoque', 'fornecedor'])
