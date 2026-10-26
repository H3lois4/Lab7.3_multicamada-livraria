from dominio import NaoEncontrado
from dominio.entidades import normalizar


class CatalogoService:
    """Casos de uso do MVP: buscar livro, ver estoque e preço, ver lojas."""

    def __init__(self, repo_livros, repo_lojas):
        self._livros = repo_livros
        self._lojas = repo_lojas

    def buscar_livros(self, termo=""):
        encontrados = [livro for livro in self._livros.listar() if livro.corresponde(termo)]
        return sorted(encontrados, key=lambda livro: normalizar(livro.titulo))

    def obter_livro(self, isbn):
        livro = self._livros.buscar_por_isbn(isbn)
        if livro is None:
            raise NaoEncontrado("Livro não encontrado")
        return livro

    def listar_lojas(self):
        return sorted(self._lojas.listar(), key=lambda loja: loja.nome)

    def obter_loja(self, loja_id):
        loja = self._lojas.buscar_por_id(loja_id)
        if loja is None:
            raise NaoEncontrado("Loja não encontrada")
        return loja

    def consultar_disponibilidade(self, isbn, loja_favorita=None):
        """Lojas que trabalham com o livro: a favorita primeiro, depois ordem alfabética."""
        livro = self.obter_livro(isbn)
        lojas = [self._lojas.buscar_por_id(loja_id) for loja_id in livro.estoque]
        lojas = sorted((l for l in lojas if l), key=lambda l: (l.id != loja_favorita, l.nome))
        return [
            {
                "loja": loja,
                "quantidade": livro.estoque[loja.id],
                "disponivel": livro.disponivel_em(loja.id),
                "favorita": loja.id == loja_favorita,
            }
            for loja in lojas
        ]

    def validar_loja_favorita(self, loja_id):
        return self.obter_loja(loja_id).id
