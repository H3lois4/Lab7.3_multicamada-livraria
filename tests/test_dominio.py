"""Camada 4 – regras de negócio puras."""
import pytest

from dominio import ErroDeNegocio, ListaDesejos, Livro


def test_busca_ignora_acentos_e_maiusculas():
    livro = Livro("1", "Memórias Póstumas", "Machado de Assis", 10)
    assert livro.corresponde("memorias") and livro.corresponde("MACHADO")
    assert not livro.corresponde("clarice")


def test_disponibilidade_por_loja():
    livro = Livro("1", "X", "Y", 10, {"a": 2, "b": 0})
    assert livro.disponivel_em("a") and not livro.disponivel_em("b")
    assert livro.disponivel_em_alguma_loja


def test_lista_de_desejos_mantem_ordem():
    lista = ListaDesejos("cliente")
    lista.adicionar("2"); lista.adicionar("1")
    assert lista.isbns == ["2", "1"]


def test_nao_aceita_livro_repetido():
    lista = ListaDesejos("cliente", ["1"])
    with pytest.raises(ErroDeNegocio, match="Livro já está na lista de desejos"):
        lista.adicionar("1")


def test_nao_remove_livro_fora_da_lista():
    with pytest.raises(ErroDeNegocio, match="Livro não está na lista de desejos"):
        ListaDesejos("cliente").remover("1")
