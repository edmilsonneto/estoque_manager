from pydantic import BaseModel
from typing import List, Optional


class ProdutoCriacao(BaseModel):
    nome: str
    quantidade: int
    preco: float


class ProdutoAtualizacao(BaseModel):
    nome: Optional[str] = None
    quantidade: Optional[int] = None
    preco: Optional[float] = None
