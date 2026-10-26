class ListaDesejosService:
    """Casos de uso da nova feature: salvar uma lista de desejos para não comprar por impulso."""

    def __init__(self, repo_listas, catalogo_service):
        self._listas = repo_listas
        self._catalogo = catalogo_service

    def adicionar(self, cliente_id, isbn):
        livro = self._catalogo.obter_livro(isbn)
        lista = self._listas.obter_do_cliente(cliente_id)
        lista.adicionar(isbn)
        self._listas.salvar(lista)
        return livro

    def remover(self, cliente_id, isbn):
        livro = self._catalogo.obter_livro(isbn)
        lista = self._listas.obter_do_cliente(cliente_id)
        lista.remover(isbn)
        self._listas.salvar(lista)
        return livro

    def contem(self, cliente_id, isbn):
        return self._listas.obter_do_cliente(cliente_id).contem(isbn)

    def listar(self, cliente_id):
        """Itens com título, autor, preço e se estão disponíveis em alguma loja."""
        lista = self._listas.obter_do_cliente(cliente_id)
        itens = []
        for isbn in lista.isbns:
            livro = self._catalogo.obter_livro(isbn)
            itens.append({"livro": livro, "disponivel": livro.disponivel_em_alguma_loja})
        return itens

    def total(self, cliente_id):
        return sum(item["livro"].preco for item in self.listar(cliente_id))
