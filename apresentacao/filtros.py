def moeda(valor):
    """Formata 1089.0 como 'R$ 1.089,00' (formatação é responsabilidade da apresentação)."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def registrar_filtros(app):
    app.add_template_filter(moeda, "moeda")
