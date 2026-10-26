"""Camada 4 – Domínio: entidades e regras de negócio. Não depende de nenhuma outra camada."""
from .entidades import ListaDesejos, Livro, Loja
from .excecoes import ErroDeNegocio, NaoEncontrado

__all__ = ["Livro", "Loja", "ListaDesejos", "ErroDeNegocio", "NaoEncontrado"]
