"""Camada 3 – casos de uso."""
import pytest

from app import criar_servicos
from dominio import ErroDeNegocio, NaoEncontrado

DOM_CASMURRO, MEMORIAS, HORA_ESTRELA = "9788535902775", "9788571641149", "9788501114775"


@pytest.fixture
def servicos():
    return criar_servicos()


# ----- MVP -----

def test_buscar_por_autor(servicos):
    assert [l.titulo for l in servicos["catalogo"].buscar_livros("machado")] == \
        ["Dom Casmurro", "Memórias Póstumas de Brás Cubas"]


def test_disponibilidade_e_preco(servicos):
    itens = {i["loja"].id: i for i in servicos["catalogo"].consultar_disponibilidade(DOM_CASMURRO)}
    assert itens["paulista"]["quantidade"] == 3 and not itens["pinheiros"]["disponivel"]


def test_favorita_aparece_primeiro(servicos):
    itens = servicos["catalogo"].consultar_disponibilidade(HORA_ESTRELA, "pinheiros")
    assert itens[0]["loja"].id == "pinheiros" and itens[0]["favorita"]


def test_sem_favorita_ordem_alfabetica(servicos):
    assert servicos["catalogo"].consultar_disponibilidade(HORA_ESTRELA)[0]["loja"].id == "paulista"


def test_horario_e_endereco(servicos):
    loja = servicos["catalogo"].obter_loja("paulista")
    assert loja.horario == "Seg a sáb, 10h às 22h; dom, 12h às 20h"


def test_loja_inexistente(servicos):
    with pytest.raises(NaoEncontrado, match="Loja não encontrada"):
        servicos["catalogo"].validar_loja_favorita("centro")


# ----- Nova feature: lista de desejos -----

def test_adicionar_e_listar_desejos(servicos):
    desejos = servicos["desejos"]
    desejos.adicionar("ana", MEMORIAS)
    desejos.adicionar("ana", DOM_CASMURRO)
    itens = desejos.listar("ana")
    assert [i["livro"].isbn for i in itens] == [MEMORIAS, DOM_CASMURRO]
    assert itens[0]["disponivel"] is False and itens[1]["disponivel"] is True
    assert desejos.total("ana") == pytest.approx(64.40)


def test_adicionar_livro_inexistente(servicos):
    with pytest.raises(NaoEncontrado, match="Livro não encontrado"):
        servicos["desejos"].adicionar("ana", "000")


def test_adicionar_repetido(servicos):
    servicos["desejos"].adicionar("ana", DOM_CASMURRO)
    with pytest.raises(ErroDeNegocio, match="Livro já está na lista de desejos"):
        servicos["desejos"].adicionar("ana", DOM_CASMURRO)


def test_remover(servicos):
    servicos["desejos"].adicionar("ana", DOM_CASMURRO)
    servicos["desejos"].remover("ana", DOM_CASMURRO)
    assert servicos["desejos"].listar("ana") == []


def test_listas_separadas_por_cliente(servicos):
    servicos["desejos"].adicionar("ana", DOM_CASMURRO)
    assert servicos["desejos"].listar("bia") == []
