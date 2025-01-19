import httpx
from typing import Any, Dict, List, Optional

API_URL = "http://localhost:8000"

def handle_response(response: httpx.Response) -> Any:
    """
    Lida com a resposta HTTP, retornando os dados ou levantando exceções em caso de erro.
    """
    if response.status_code in {200, 201}:
        return response.json()
    response.raise_for_status()

async def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None
) -> Any:
    """
    Faz uma requisição HTTP genérica usando httpx.AsyncClient.

    :param method: Método HTTP (GET, POST, PUT, etc.).
    :param endpoint: Endpoint da API (relativo ao API_URL).
    :param data: Dados JSON opcionais para envio.
    :return: Resposta processada ou erro levantado.
    """
    url = f"{API_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, json=data)
        return handle_response(response)

async def fetch_produtos() -> List[Dict]:
    """Obtém a lista de produtos do estoque."""
    try:
        data = await make_request("GET", "/estoque")
        return data.get("produtos", [])
    except httpx.HTTPError as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

async def adicionar_produto_async(produto: Dict) -> Optional[Dict]:
    """Adiciona um novo produto ao estoque."""
    try:
        return await make_request("POST", "/produto", data=produto)
    except httpx.HTTPError as e:
        print(f"Erro ao adicionar produto: {e}")
        return None

async def atualizar_produto_async(produto: Dict) -> Optional[Dict]:
    """Atualiza um produto existente no estoque."""
    try:
        return await make_request("PUT", f"/produto/{produto['id']}", data=produto)
    except httpx.HTTPError as e:
        print(f"Erro ao atualizar produto: {e}")
        return None

async def entrada_estoque(produto_id: int, quantidade: int) -> Optional[Dict]:
    """Registra a entrada de um produto no estoque."""
    try:
        return await make_request("POST", "/entrada", params={"produto_id": produto_id, "quantidade": quantidade})
    except httpx.HTTPError as e:
        print(f"Erro ao registrar entrada no estoque: {e}")
        return None

async def saida_estoque(produto_id: int, quantidade: int) -> Optional[Dict]:
    """Registra a saída de um produto no estoque."""
    try:
        return await make_request("POST", "/saida", params={"produto_id": produto_id, "quantidade": quantidade})
    except httpx.HTTPError as e:
        print(f"Erro ao registrar saída do estoque: {e}")
        return None