# app/modules/previdenciario/__init__.py - ATUALIZADO
from .schemas import DadosPrevidenciarios, PeticaoPrevidenciaria
from .service import PrevidenciarioService

__all__ = [
    "DadosPrevidenciarios",
    "PeticaoPrevidenciaria",
    "PrevidenciarioService"
]