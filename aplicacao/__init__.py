"""Camada 3 – Aplicação: casos de uso que coordenam domínio e repositórios."""
from .catalogo_service import CatalogoService
from .lista_desejos_service import ListaDesejosService

__all__ = ["CatalogoService", "ListaDesejosService"]
