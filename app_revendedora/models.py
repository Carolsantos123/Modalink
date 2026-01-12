from django.db import models
from django.utils import timezone

# ----- Produto no estoque (peça cadastrada pela loja) -----
class Produto(models.Model):
    # ID do documento no Firebase (opcional) para sincronização
    firebase_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID do produto no Firebase")

    # Código único da peça (fornecido pela loja)
    codigo = models.CharField(max_length=100, unique=True, help_text="Código único da peça")

    # Nome descritivo da peça
    nome = models.CharField(max_length=255)

    # Tamanho (ex: P, M, G, 38, 40) - opcional
    tamanho = models.CharField(max_length=30, blank=True, null=True)

    # Preço unitário atual
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # Quantidade em estoque (controlada pela loja)
    quantidade_estoque = models.PositiveIntegerField(default=0)

    # Algumas etiquetas/observações (ex: cor, marca) - opcional
    observacoes = models.TextField(blank=True, null=True)

    # Data de cadastro/última atualização
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.tamanho or 'Tamanho N/A'})"

# ----- Seleção (carrinho) que a revendedora monta ao escolher peças -----
class SelecionItem(models.Model):
    """
    Modelo temporário que representa o 'carrinho' de uma revendedora.
    A loja revisará e transformará em 'Sacola' quando confirmar.
    """
    revendedora = models.ForeignKey(
        "Revendedora", on_delete=models.CASCADE, related_name="selecoes"
    )
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    # preço_snapshot guarda o preço no momento da seleção (para histórico)
    preco_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    data_selecao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("revendedora", "produto")  # evita duplicar a mesma peça no carrinho

    def __str__(self):
        return f"{self.revendedora.nome} selecionou {self.produto.codigo} x{self.quantidade}"

# ----- Sacola (a loja cria e separa a sacola para a revendedora) -----
STATUS_SACOLA = [
    ("pendente", "Pendente"),     # sacola criada, ainda não separada
    ("separada", "Separada"),     # loja já separou os itens
    ("entregue", "Entregue"),     # entregou para revendedora
    ("cancelada", "Cancelada"),   # cancelada
]

class Sacola(models.Model):
    # vínculo com a revendedora que receberá a sacola
    revendedora = models.ForeignKey("Revendedora", on_delete=models.CASCADE, related_name="sacolas")

    # opcional: se quiser referenciar a nota fiscal usada na compra/entrada (não obrigatório)
    nota_fiscal = models.ForeignKey("NotaFiscal", on_delete=models.SET_NULL, blank=True, null=True)

    # identificação/etiqueta da sacola (pode ser um código gerado)
    codigo = models.CharField(max_length=100, unique=True)

    # status da sacola
    status = models.CharField(max_length=20, choices=STATUS_SACOLA, default="pendente")

    # data de criação e data de atualização
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # valor total calculado (snapshot) - opcional, calculado quando a sacola é finalizada
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # observações da loja (ex: observações na separação)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sacola {self.codigo} - {self.revendedora.nome}"

    def calcular_valor_total(self):
        """
        Calcula e atualiza o valor_total com base nos itens atuais da sacola.
        Chame este método quando a sacola for finalizada ou ao modificar itens.
        """
        total = sum([item.preco_unitario * item.quantidade for item in self.itens.all()])
        self.valor_total = total
        self.save(update_fields=["valor_total"])
        return total

# ----- Item da sacola (snapshot do produto no momento da separação) -----
class SacolaItem(models.Model):
    sacola = models.ForeignKey(Sacola, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)

    # preço_unitario aqui é um snapshot do preço quando o item entrou na sacola
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    # status individual do item (ex: separado, indisponivel)
    status_item = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.produto.codigo} x{self.quantidade} em {self.sacola.codigo}"
