# app/modules/processual_civil/__init__.py - CRIAR
from .schemas import DadosProcessualCivil, PeticaoProcessualCivil
from .service import ProcessualCivilService

__all__ = [
    "DadosProcessualCivil",
    "PeticaoProcessualCivil",
    "ProcessualCivilService"
]