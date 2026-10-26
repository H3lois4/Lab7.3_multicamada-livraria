"""Camadas 1 e 2 – rotas HTTP e páginas renderizadas."""
import pytest

from app import create_app

DOM_CASMURRO, HORA_ESTRELA = "9788535902775", "9788501114775"


@pytest.fixture
def cliente():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def texto(resposta):
    return resposta.get_data(as_text=True)


def test_busca(cliente):
    html = texto(cliente.get("/?q=clarice"))
    assert "A Hora da Estrela" in html and "R$ 39,90" in html and "Dom Casmurro" not in html


def test_detalhe_mostra_estoque(cliente):
    html = texto(cliente.get(f"/livros/{DOM_CASMURRO}"))
    assert "3 em estoque" in html and "Esgotado" in html


def test_livro_inexistente_404(cliente):
    resposta = cliente.get("/livros/000")
    assert resposta.status_code == 404 and "Livro não encontrado" in texto(resposta)


def test_loja(cliente):
    assert "Rua dos Pinheiros, 500" in texto(cliente.get("/lojas/pinheiros"))
    assert cliente.get("/lojas/centro").status_code == 404


def test_favoritar(cliente):
    cliente.post("/lojas/pinheiros/favorita")
    html = texto(cliente.get(f"/livros/{HORA_ESTRELA}"))
    assert html.index("Livraria Pinheiros") < html.index("Livraria Paulista")


def test_lista_de_desejos_pela_interface(cliente):
    assert "Sua lista está vazia" in texto(cliente.get("/desejos/"))
    html = texto(cliente.post(f"/desejos/{DOM_CASMURRO}", follow_redirects=True))
    assert "Dom Casmurro foi salvo na sua lista de desejos." in html
    assert "Total da lista: R$ 29,90" in html


def test_desejo_repetido_mostra_erro(cliente):
    cliente.post(f"/desejos/{DOM_CASMURRO}")
    html = texto(cliente.post(f"/desejos/{DOM_CASMURRO}", follow_redirects=True))
    assert "Livro já está na lista de desejos" in html


def test_remover_desejo(cliente):
    cliente.post(f"/desejos/{DOM_CASMURRO}")
    html = texto(cliente.post(f"/desejos/{DOM_CASMURRO}/remover", follow_redirects=True))
    assert "Sua lista está vazia" in html


def test_detalhe_mostra_botao_conforme_lista(cliente):
    assert "Salvar na lista de desejos" in texto(cliente.get(f"/livros/{DOM_CASMURRO}"))
    cliente.post(f"/desejos/{DOM_CASMURRO}")
    assert "Remover da lista de desejos" in texto(cliente.get(f"/livros/{DOM_CASMURRO}"))
