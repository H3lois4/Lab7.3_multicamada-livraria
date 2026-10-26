"""Camada 5 – repositórios."""
from dados import RepositorioListasDesejos, RepositorioLivros, RepositorioLojas, popular_dados_iniciais


def test_dados_iniciais():
    lojas, livros = RepositorioLojas(), RepositorioLivros()
    popular_dados_iniciais(lojas, livros)
    assert len(lojas.listar()) == 2 and len(livros.listar()) == 4
    assert livros.buscar_por_isbn("9788535902775").titulo == "Dom Casmurro"
    assert lojas.buscar_por_id("centro") is None


def test_cada_cliente_tem_sua_lista():
    repo = RepositorioListasDesejos()
    repo.obter_do_cliente("ana").adicionar("1")
    assert repo.obter_do_cliente("ana").isbns == ["1"]
    assert repo.obter_do_cliente("bia").isbns == []
