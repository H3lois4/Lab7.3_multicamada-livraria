"""Camada 5 – Dados: repositórios que guardam e recuperam entidades do domínio."""
from .repositorios import RepositorioListasDesejos, RepositorioLivros, RepositorioLojas
from .seed import popular_dados_iniciais

__all__ = ["RepositorioLivros", "RepositorioLojas", "RepositorioListasDesejos",
           "popular_dados_iniciais"]
