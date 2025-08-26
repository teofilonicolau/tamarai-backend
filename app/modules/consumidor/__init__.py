# app/modules/consumidor/__init__.py - ATUALIZADO
from .schemas import DadosConsumidor, PeticaoConsumidor
from .service import ConsumidorService

__all__ = [
    "DadosConsumidor",
    "PeticaoConsumidor",
    "ConsumidorService"
]