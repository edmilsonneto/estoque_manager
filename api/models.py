from pydantic import BaseModel
from typing import List, Optional

class Produto(BaseModel):
    id: int
    nome: str
    quantidade: int
    preco: float

class Estoque(BaseModel):
    produtos: List[Produto]
