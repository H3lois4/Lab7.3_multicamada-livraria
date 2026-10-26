"""Armazenamento em memória. Para usar um banco de dados, basta criar
classes com os mesmos métodos; as camadas de cima não mudam."""
from dominio import ListaDesejos


class RepositorioLojas:
    def __init__(self):
        self._lojas = {}

    def salvar(self, loja):
        self._lojas[loja.id] = loja

    def buscar_por_id(self, loja_id):
        return self._lojas.get(loja_id)

    def listar(self):
        return list(self._lojas.values())


class RepositorioLivros:
    def __init__(self):
        self._livros = {}

    def salvar(self, livro):
        self._livros[livro.isbn] = livro

    def buscar_por_isbn(self, isbn):
        return self._livros.get(isbn)

    def listar(self):
        return list(self._livros.values())


class RepositorioListasDesejos:
    def __init__(self):
        self._listas = {}

    def obter_do_cliente(self, cliente_id):
        return self._listas.setdefault(cliente_id, ListaDesejos(cliente_id))

    def salvar(self, lista):
        self._listas[lista.cliente_id] = lista
