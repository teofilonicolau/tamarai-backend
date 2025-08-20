# app/models/__init__.py
from .base import Base
from .consulta import Consulta, AreaJuridica
from .peticao import Peticao, TipoPeticao, StatusPeticao
from .documento import Documento

__all__ = [
    "Base",
    "Consulta", 
    "AreaJuridica",
    "Peticao", 
    "TipoPeticao", 
    "StatusPeticao",
    "Documento"
]