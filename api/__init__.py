"""Camada 2 – API/Controle: rotas HTTP. Recebe a requisição, chama a camada de
aplicação e devolve a resposta. Não contém regra de negócio."""
from .desejos_controller import desejos_bp
from .livros_controller import livros_bp
from .lojas_controller import lojas_bp

__all__ = ["livros_bp", "lojas_bp", "desejos_bp"]
