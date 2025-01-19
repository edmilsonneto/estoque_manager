from reactpy import component, html, use_state, use_effect, event

@component
def CadastroProduto(on_submit, produto=None):
    """
    Componente para cadastrar ou editar um produto.

    :param on_submit: Função chamada ao enviar o formulário.
    :param produto: Produto em edição (opcional).
    """
    nome, set_nome = use_state(produto["nome"] if produto else "")
    quantidade, set_quantidade = use_state(produto["quantidade"] if produto else "")
    preco, set_preco = use_state(produto["preco"] if produto else "")

    use_effect(lambda: set_nome(produto["nome"] if produto else ""), [produto])
    use_effect(lambda: set_quantidade(produto["quantidade"] if produto else ""), [produto])
    use_effect(lambda: set_preco(produto["preco"] if produto else ""), [produto])

    @event(prevent_default=True)
    async def handle_submit(event):  # Agora é assíncrona
        if nome and quantidade and preco:
            produto_dados = {
                "id": produto["id"] if produto else None,
                "nome": nome,
                "quantidade": int(quantidade),
                "preco": float(preco),
            }
            await on_submit(produto_dados)  # Aguardando a função assíncrona
            set_nome("")
            set_quantidade("")
            set_preco("")

    def render_input(label, input_type, value, on_change, step=None):
        return html.div(
            {"className": "mb-4"},
            html.label({"className": "block text-gray-700 mb-1"}, label),
            html.input(
                {
                    "type": input_type,
                    "value": value,
                    "onChange": lambda e: on_change(e["target"]["value"]),
                    "step": step,
                    "className": "w-full p-2 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                }
            )
        )

    return html.form(
        {"onSubmit": handle_submit, "className": "space-y-4"},
        render_input("Nome:", "text", nome, set_nome),
        render_input("Quantidade:", "number", quantidade, set_quantidade),
        render_input("Preço:", "number", preco, set_preco, step="0.01"),
        html.div(
            {"class_name": "flex justify-end"},
            html.button(
                {
                    "type": "submit",
                    "class_name": "px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                },
                "Salvar" if produto else "Adicionar Produto"
            )
        )
    )
