from fastapi import FastAPI
from reactpy import component, html, use_state
from front.components.cadastro_produto.cadastro_produto import CadastroProduto
from front.components.entrada_saida_estoque.entrada_saida_estoque import EntradaSaidaEstoque
from front.components.lista_estoque.lista_estoque import ListaEstoque
from front.service.api_service import adicionar_produto_async, atualizar_produto_async, fetch_produtos
from reactpy.backend.fastapi import configure

cdn_1 = html.link({
    "href": "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
    "rel": "stylesheet"
})

def atualizar_lista_produtos(lista, produto_atualizado):
    """Atualiza a lista de produtos com o produto editado."""
    return [
        produto_atualizado if str(produto["id"]) == str(produto_atualizado["id"]) else produto
        for produto in lista
    ]

@component
def App():
    produtos, set_produtos = use_state([])
    produto_em_edicao, set_produto_em_edicao = use_state(None)

    async def salvar_produto(produto):
        """Adiciona ou edita um produto na lista."""
        try:
            if produto.get("id"):
                produto_editado = await atualizar_produto_async(produto)
                set_produtos(lambda lista: atualizar_lista_produtos(lista, produto_editado))
            else:
                produto_adicionado = await adicionar_produto_async(produto)
                set_produtos(lambda lista: lista + [produto_adicionado])
            set_produto_em_edicao(None)
        except Exception as e:
            print(f"Erro ao salvar produto: {e}")

    return html.div(
        cdn_1,
        html.div(
            {"className": "max-w-4xl mx-auto bg-white p-6 rounded-lg shadow"},
            html.h1(
                {"className": "text-2xl font-bold text-gray-800 mb-4"},
                "Gerenciador de Produtos"
            ),
            CadastroProduto(
                on_submit=salvar_produto,
                produto=produto_em_edicao
            ),
            ListaEstoque(
                produtos=produtos,
                set_produtos=set_produtos,
                on_edit=set_produto_em_edicao
            ),
            html.br(),
            html.br(),
            html.h1(
                {"className": "text-2xl font-bold text-gray-800 mb-4"},
                "Gerenciador de Estoque"
            ),
            EntradaSaidaEstoque()
        )
    )

# Configuração do FastAPI
app = FastAPI()

configure(app, App)
