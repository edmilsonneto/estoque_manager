from typing import List, Dict
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from api.models import Estoque, Produto
from api.schemas import ProdutoCriacao, ProdutoAtualizacao


estoque: List[Dict] = []


def get_estoque():
    return estoque


def add_produto(produto: dict):
    estoque.append(produto)


def update_produto(id: int, produto_atualizado: dict):
    for i, prod in enumerate(estoque):
        if prod['id'] == str(id):
            estoque[i] = produto_atualizado
            break


def delete_produto(id: int):
    global estoque
    estoque = [prod for prod in estoque if prod['id'] != id]


def get_produto_by_id(id: int):
    for prod in estoque:
        if prod['id'] == str(id):
            return prod
    return None
