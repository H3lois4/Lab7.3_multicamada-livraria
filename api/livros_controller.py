from flask import Blueprint, abort, render_template, request

from dominio import NaoEncontrado

from .contexto import catalogo, cliente_id, desejos, loja_favorita

livros_bp = Blueprint("livros", __name__)


@livros_bp.get("/")
def buscar():
    termo = request.args.get("q", "")
    return render_template("livros/busca.html", livros=catalogo().buscar_livros(termo), termo=termo)


@livros_bp.get("/livros/<isbn>")
def detalhe(isbn):
    try:
        livro = catalogo().obter_livro(isbn)
        lojas = catalogo().consultar_disponibilidade(isbn, loja_favorita())
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("livros/detalhe.html", livro=livro, lojas=lojas,
                           na_lista=desejos().contem(cliente_id(), isbn))
