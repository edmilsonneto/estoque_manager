from reactpy import component, html, use_effect, use_state
from service.api_service import fetch_produtos
import asyncio

@component
def ListaEstoque(produtos, set_produtos, on_edit):
    async def obter_produtos():
        try:
            produtos_obtidos = await fetch_produtos()
            set_produtos(produtos_obtidos)
        except Exception as e:
            print(f"Erro ao obter produtos: {e}")

    def carregar_produtos():
        asyncio.create_task(obter_produtos())

    use_effect(carregar_produtos, [])

    def handle_edit(produto):
        on_edit(produto)

    def handle_delete(produto):
        # Lógica para deletar o produto
        pass

    def render_linha(produto):
        return html.tr(
            {"key": f"produto-{produto['id']}", "className": "border-t"},
            html.td({"className": "px-4 py-2"}, produto['nome']),
            html.td({"className": "px-4 py-2 text-center"}, produto['quantidade']),
            html.td({"className": "px-4 py-2 text-center"}, f"R${produto['preco']:.2f}"),
            html.td(
                {"className": "px-4 py-2 flex space-x-2 justify-center"},
                html.button(
                    {
                        "onClick": lambda _: handle_edit(produto),
                        "className": "px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                    },
                    "Editar"
                ),
                html.button(
                    {
                        "onClick": lambda _: handle_delete(produto),
                        "className": "px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                    },
                    "Excluir"
                )
            )
        )

    return html.table(
        {"className": "w-full border-collapse border border-gray-200 mt-6"},
        html.thead(
            {"className": "bg-gray-100"},
            html.tr(
                html.th({"className": "px-4 py-2"}, "Nome"),
                html.th({"className": "px-4 py-2 text-center"}, "Quantidade"),
                html.th({"className": "px-4 py-2 text-center"}, "Preço"),
                html.th({"className": "px-4 py-2 text-center"}, "Ações")
            )
        ),
        html.tbody([render_linha(produto) for produto in produtos])
    )