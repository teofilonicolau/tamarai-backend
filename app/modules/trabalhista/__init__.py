# app/modules/trabalhista/__init__.py
from .schemas import DadosTrabalhistas, PeticaoTrabalhista
from .service import TrabalhistaService

__all__ = [
    "DadosTrabalhistas",
    "PeticaoTrabalhista", 
    "TrabalhistaService"
]