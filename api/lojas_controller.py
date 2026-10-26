from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from dominio import NaoEncontrado

from .contexto import catalogo, loja_favorita

lojas_bp = Blueprint("lojas", __name__, url_prefix="/lojas")


@lojas_bp.get("/")
def listar():
    return render_template("lojas/lista.html", lojas=catalogo().listar_lojas(),
                           favorita=loja_favorita())


@lojas_bp.get("/<loja_id>")
def detalhe(loja_id):
    try:
        loja = catalogo().obter_loja(loja_id)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("lojas/detalhe.html", loja=loja, favorita=loja_favorita())


@lojas_bp.post("/<loja_id>/favorita")
def favoritar(loja_id):
    try:
        session["loja_favorita"] = catalogo().validar_loja_favorita(loja_id)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    flash(f"{catalogo().obter_loja(loja_id).nome} agora é sua loja favorita.")
    return redirect(request.form.get("voltar") or url_for("lojas.listar"))
