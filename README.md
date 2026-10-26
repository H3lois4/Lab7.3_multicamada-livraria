# Livraria – Arquitetura Multicamadas

Evolução do MVP da livraria (repositório MVC do exercício 7.2) para a arquitetura
em 5 camadas desenhada no exercício 7.1, com uma **nova feature: lista de desejos**.

## Camadas

| # | Camada | Pasta | Responsabilidade |
|---|---|---|---|
| 1 | Apresentação | `apresentacao/` | Templates Jinja, CSS e formatação (ex.: `R$ 29,90`) |
| 2 | API / Controle | `api/` | Rotas Flask: recebem a requisição, chamam os serviços e escolhem a página |
| 3 | Aplicação | `aplicacao/` | Casos de uso: `CatalogoService` e `ListaDesejosService` |
| 4 | Domínio | `dominio/` | Entidades (`Livro`, `Loja`, `ListaDesejos`) e regras de negócio |
| 5 | Dados | `dados/` | Repositórios em memória e dados iniciais |

`app.py` é o ponto de composição: cria os repositórios, injeta nos serviços e registra as rotas.

**Regra de dependência:** cada camada usa apenas as de baixo, e o domínio não depende de
nenhuma. Isso é verificado automaticamente em `tests/test_arquitetura.py`.

## Funcionalidades

- Consultar o estoque do livro em cada loja (MVP)
- Ver o preço praticado (MVP)
- Ver horário e endereço das lojas (MVP)
- Escolher loja favorita, que aparece primeiro (MVP)
- **Nova:** lista de desejos – salvar, remover, ver disponibilidade e o total da lista

## O que mudou em relação ao MVC

| MVC (7.2) | Multicamadas (7.3) |
|---|---|
| `views/`, `static/` | `apresentacao/` |
| `controllers/` | `api/` |
| `models/catalogo.py` (regras + armazenamento juntos) | separado em `aplicacao/`, `dominio/` e `dados/` |
| `Livro.preco_formatado` no model | filtro `moeda` na apresentação |

## Como rodar

```bash
pip install -r requirements.txt
pytest -v        # testes por camada + teste de arquitetura
python app.py    # http://localhost:5000
```
