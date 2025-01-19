from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from typing import List
from api.models import Estoque, Produto
from api.schemas import ProdutoCriacao, ProdutoAtualizacao
from api.database import (get_estoque, add_produto, update_produto, delete_produto,
                      get_produto_by_id)

app = FastAPI(title="Estoque API")


@app.get("/estoque", response_model=Estoque)
async def get_resumo():
    produtos = get_estoque()
    return {"produtos": produtos}


@app.post("/produto", status_code=201)
async def criar_produto(produto: ProdutoCriacao):
    novo_produto = {
        "id": str(uuid4().int)[:12],
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "preco": produto.preco,
        "criado_em": datetime.now().isoformat()
    }
    add_produto(novo_produto)
    return novo_produto


@app.put("/produto/{id}")
async def atualizar_produto(id: str, produto_atualizado: ProdutoAtualizacao):
    produto_existente = get_produto_by_id(int(id))
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_atualizado_dict = produto_atualizado.dict(exclude_unset=True)
    produto_atualizado_completo = {
        **produto_existente,
        **produto_atualizado_dict
    }
    update_produto(int(id), produto_atualizado_completo)
    return produto_atualizado_completo


@app.delete("/produto/{id}", status_code=204)
async def deletar_produto(id: str):
    produto_existente = get_produto_by_id(int(id))
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    delete_produto(int(id))
    return {"message": "Produto deletado com sucesso"}


@app.get("/produto/{id}", response_model=Produto)
async def get_produto_por_id(id: str):
    produto = get_produto_by_id(int(id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.post("/entrada", status_code=201)
async def registrar_entrada(produto_id: int, quantidade: int):
    produto = get_produto_by_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    novo_total = produto["quantidade"] + quantidade
    update_produto(produto_id, {**produto, "quantidade": novo_total})
    return {"message": f"Entrada registrada. Novo total: {novo_total}"}


@app.post("/saida", status_code=201)
async def registrar_saida(produto_id: int, quantidade: int):
    produto = get_produto_by_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if produto["quantidade"] < quantidade:
        raise HTTPException(status_code=400,
                            detail="Quantidade insuficiente em estoque")

    novo_total = produto["quantidade"] - quantidade
    update_produto(produto_id, {**produto, "quantidade": novo_total})
    return {"message": f"Saida registrada. Novo total: {novo_total}"}
