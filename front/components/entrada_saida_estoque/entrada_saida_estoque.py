from reactpy import component, event, use_state, html
from front.service.api_service import entrada_estoque, saida_estoque


@component
def EntradaSaidaEstoque():
    """Componente para gerenciar entradas e saídas de estoque."""
    produto_id, set_produto_id = use_state("")
    quantidade, set_quantidade = use_state("")

    @event(prevent_default=True)
    async def handle_entrada():
        if produto_id and quantidade:
            response = await entrada_estoque(int(produto_id), int(quantidade))
            if response:
                print(f"Entrada registrada: {response}")
                set_produto_id("")
                set_quantidade("")

    @event(prevent_default=True)
    async def handle_saida():
        if produto_id and quantidade:
            response = await saida_estoque(int(produto_id), int(quantidade))
            if response:
                print(f"Saída registrada: {response}")
                set_produto_id("")
                set_quantidade("")

    def render_input(label, value, on_change):
        return html.div(
            {"className": "mb-4"},
            html.label({"className": "block text-gray-700 mb-1"}, label),
            html.input(
                {
                    "type": "number",
                    "value": value,
                    "onChange": lambda e: on_change(e["target"]["value"]),
                    "className": "w-full p-2 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                }
            )
        )

    return html.div(
        {"className": "space-y-4"},
        render_input("Produto ID:", produto_id, set_produto_id),
        render_input("Quantidade:", quantidade, set_quantidade),
        html.div(
            {"className": "flex space-x-4"},
            html.button(
                {"type": "button", "onClick": handle_entrada, "className": "px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"},
                "Registrar Entrada"
            ),
            html.button(
                {"type": "button", "onClick": handle_saida, "className": "px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"},
                "Registrar Saída"
            )
        )
    )