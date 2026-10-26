from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from dominio import ErroDeNegocio, NaoEncontrado

from .contexto import cliente_id, desejos

desejos_bp = Blueprint("desejos", __name__, url_prefix="/desejos")


@desejos_bp.get("/")
def listar():
    return render_template("desejos/lista.html", itens=desejos().listar(cliente_id()),
                           total=desejos().total(cliente_id()))


@desejos_bp.post("/<isbn>")
def adicionar(isbn):
    try:
        livro = desejos().adicionar(cliente_id(), isbn)
        flash(f"{livro.titulo} foi salvo na sua lista de desejos.")
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    except ErroDeNegocio as erro:
        flash(str(erro), "erro")
    return redirect(request.form.get("voltar") or url_for("desejos.listar"))


@desejos_bp.post("/<isbn>/remover")
def remover(isbn):
    try:
        livro = desejos().remover(cliente_id(), isbn)
        flash(f"{livro.titulo} foi removido da sua lista de desejos.")
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    except ErroDeNegocio as erro:
        flash(str(erro), "erro")
    return redirect(request.form.get("voltar") or url_for("desejos.listar"))
