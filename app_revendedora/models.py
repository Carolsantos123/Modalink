from django.db import models
# Importa o módulo de modelos do Django, que permite criar tabelas no banco de dados.

# Lista de opções possíveis para o campo "status"
STATUS_CHOICES = [
    ("ativa", "Ativa"),         # Revendedora está ativa e trabalhando
    ("inativa", "Inativa"),     # Não trabalha mais
    ("pendente", "Pendente"),   # Ainda não aprovada / documentos faltando
]

class Revendedora(models.Model):
    # O nome completo da revendedora
    nome = models.CharField(max_length=255)
    
    # CPF será único, impedindo dois cadastros iguais
    cpf = models.CharField(max_length=14, unique=True)
    
    # Telefone é opcional (blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    # Endereço da revendedora — todos os campos abaixo são opcionais
    endereco = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)  # Ex.: SP, RJ, BA
    cep = models.CharField(max_length=10, blank=True, null=True)

    # Data de nascimento — também pode ser deixada em branco
    dataNascimento = models.DateField(blank=True, null=True)

    # E-mail da revendedora
    email = models.EmailField(blank=True, null=True)

    # Upload de imagens — Django guarda apenas o caminho da imagem
    fotoDocumento = models.ImageField(
        upload_to="revendedoras/docs/",  # Pasta onde será armazenado
        blank=True,
        null=True
    )

    fotoPerfil = models.ImageField(
        upload_to="revendedoras/perfis/",  # Outra pasta para fotos de perfil
        blank=True,
        null=True
    )

    # Data em que o cadastro foi criado automaticamente
    dataCadastro = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True → salva a data/hora automaticamente na criação

    # Status da revendedora com opções definidas lá em cima
    status = models.CharField(
        max_length=10,          # Tamanho máximo do texto
        choices=STATUS_CHOICES, # Lista de opções
        default="pendente"      # Valor padrão
    )

    # Como o objeto será exibido no admin ou no terminal
    def __str__(self):
        # Retorna o nome e o CPF para fácil identificação
        return f"{self.nome} ({self.cpf})"

