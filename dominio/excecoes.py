class ErroDeNegocio(Exception):
    """Violação de uma regra de negócio."""


class NaoEncontrado(ErroDeNegocio):
    """Livro ou loja inexistente."""
