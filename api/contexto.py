"""Acesso aos serviços e à identificação do cliente na sessão."""
import uuid

from flask import current_app, session


def catalogo():
    return current_app.config["SERVICOS"]["catalogo"]


def desejos():
    return current_app.config["SERVICOS"]["desejos"]


def cliente_id():
    if "cliente_id" not in session:
        session["cliente_id"] = uuid.uuid4().hex
    return session["cliente_id"]


def loja_favorita():
    return session.get("loja_favorita")
