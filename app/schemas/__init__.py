# app/schemas/__init__.py 
from .consulta import ConsultaCreate, ConsultaResponse, ConsultaEspecializada
from .peticao import PeticaoCreate, PeticaoResponse, PeticaoAprovacao, DadosAutor, DadosBeneficioPrevidenciario, DadosConsumidor, PedidosPeticao
from app.modules.trabalhista.schemas import DadosTrabalhistas, PeticaoTrabalhista

__all__ = [
    "ConsultaCreate",
    "ConsultaResponse", 
    "ConsultaEspecializada",
    "PeticaoCreate",
    "PeticaoResponse",
    "PeticaoAprovacao",
    "DadosAutor",
    "DadosBeneficioPrevidenciario", 
    "DadosConsumidor",
    "PedidosPeticao",
    "DadosTrabalhistas",
    "PeticaoTrabalhista"
]