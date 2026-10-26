"""Ponto de entrada: monta a aplicação ligando as 5 camadas.

  1. apresentacao/  →  templates, estilos e formatação
  2. api/           →  rotas HTTP (controle)
  3. aplicacao/     →  casos de uso (serviços)
  4. dominio/       →  entidades e regras de negócio
  5. dados/         →  repositórios e dados iniciais
"""
from flask import Flask, render_template

from api import desejos_bp, livros_bp, lojas_bp
from aplicacao import CatalogoService, ListaDesejosService
from apresentacao import registrar_filtros
from dados import (RepositorioListasDesejos, RepositorioLivros, RepositorioLojas,
                   popular_dados_iniciais)


def criar_servicos():
    repo_lojas, repo_livros = RepositorioLojas(), RepositorioLivros()
    popular_dados_iniciais(repo_lojas, repo_livros)
    catalogo = CatalogoService(repo_livros, repo_lojas)
    desejos = ListaDesejosService(RepositorioListasDesejos(), catalogo)
    return {"catalogo": catalogo, "desejos": desejos}


def create_app():
    app = Flask(__name__, template_folder="apresentacao/templates",
                static_folder="apresentacao/static")
    app.config["SECRET_KEY"] = "troque-esta-chave"
    app.config["SERVICOS"] = criar_servicos()

    registrar_filtros(app)
    for blueprint in (livros_bp, lojas_bp, desejos_bp):
        app.register_blueprint(blueprint)

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return render_template("erro.html", mensagem=erro.description), 404

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
