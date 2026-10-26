import unicodedata
from dataclasses import dataclass, field

from .excecoes import ErroDeNegocio


def normalizar(texto):
    """Remove acentos e diferenças entre maiúsculas e minúsculas."""
    sem_acentos = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sem_acentos if not unicodedata.combining(c)).casefold().strip()


@dataclass(frozen=True)
class Loja:
    id: str
    nome: str
    endereco: str
    horario: str


@dataclass
class Livro:
    isbn: str
    titulo: str
    autor: str
    preco: float
    estoque: dict = field(default_factory=dict)  # {loja_id: quantidade}

    def corresponde(self, termo):
        """Regra de busca: trecho do título ou do autor, sem diferenciar acentos."""
        termo = normalizar(termo)
        return termo in normalizar(self.titulo) or termo in normalizar(self.autor)

    def disponivel_em(self, loja_id):
        return self.estoque.get(loja_id, 0) > 0

    @property
    def disponivel_em_alguma_loja(self):
        return any(qtd > 0 for qtd in self.estoque.values())


@dataclass
class ListaDesejos:
    """Nova feature: lista de desejos do cliente, na ordem em que os livros foram salvos."""
    cliente_id: str
    isbns: list = field(default_factory=list)

    def adicionar(self, isbn):
        if isbn in self.isbns:
            raise ErroDeNegocio("Livro já está na lista de desejos")
        self.isbns.append(isbn)

    def remover(self, isbn):
        if isbn not in self.isbns:
            raise ErroDeNegocio("Livro não está na lista de desejos")
        self.isbns.remove(isbn)

    def contem(self, isbn):
        return isbn in self.isbns
