"""Garante a regra da arquitetura: cada camada só importa as camadas permitidas."""
import ast
import pathlib

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CAMADAS = ["apresentacao", "api", "aplicacao", "dominio", "dados"]
PERMITIDO = {
    "apresentacao": set(),
    "api": {"dominio"},            # usa serviços via app.config e exceções do domínio
    "aplicacao": {"dominio"},      # recebe os repositórios por injeção
    "dominio": set(),              # núcleo: não depende de ninguém
    "dados": {"dominio"},
}


def camadas_importadas(pasta):
    usadas = set()
    for arquivo in (RAIZ / pasta).rglob("*.py"):
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            nomes = [a.name for a in no.names] if isinstance(no, ast.Import) else \
                    [no.module or ""] if isinstance(no, ast.ImportFrom) and no.level == 0 else []
            usadas |= {n.split(".")[0] for n in nomes if n.split(".")[0] in CAMADAS}
    return usadas - {pasta}


@pytest.mark.parametrize("camada", CAMADAS)
def test_dependencias_entre_camadas(camada):
    assert camadas_importadas(camada) <= PERMITIDO[camada]
