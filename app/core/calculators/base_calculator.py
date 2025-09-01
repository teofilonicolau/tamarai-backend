# app/core/calculators/base_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, Union
import math

class BaseCalculator:
    
    def calcular_juros_mora(self, valor_principal: float, data_vencimento: date, 
                           taxa_mensal: float = 0.01) -> Dict[str, Any]:
        """Calcula juros de mora"""
        hoje = date.today()
        dias_atraso = (hoje - data_vencimento).days
        
        if dias_atraso <= 0:
            return {
                "dias_atraso": 0,
                "juros": 0,
                "valor_total": valor_principal
            }
        
        meses_atraso = dias_atraso / 30
        juros = valor_principal * taxa_mensal * meses_atraso
        
        return {
            "valor_principal": valor_principal,
            "dias_atraso": dias_atraso,
            "meses_atraso": round(meses_atraso, 2),
            "taxa_mensal": f"{taxa_mensal * 100}%",
            "valor_juros": round(juros, 2),
            "valor_total": round(valor_principal + juros, 2)
        }
    
    def aplicar_correcao_monetaria(self, valor: float, data_inicial: date, 
                                  indice: str = "INPC") -> Dict[str, Any]:
        """Aplica correção monetária (simulada)"""
        hoje = date.today()
        anos_decorridos = (hoje - data_inicial).days / 365
        
        # Índices simulados (em produção, buscar de API oficial)
        indices_anuais = {
            "INPC": 0.045,    # 4.5% ao ano
            "IPCA": 0.042,    # 4.2% ao ano
            "SELIC": 0.105    # 10.5% ao ano
        }
        
        taxa_anual = indices_anuais.get(indice, 0.045)
        fator_correcao = (1 + taxa_anual) ** anos_decorridos
        valor_corrigido = valor * fator_correcao
        
        return {
            "valor_original": valor,
            "data_inicial": data_inicial.isoformat(),
            "data_final": hoje.isoformat(),
            "anos_decorridos": round(anos_decorridos, 2),
            "indice_utilizado": indice,
            "taxa_anual": f"{taxa_anual * 100}%",
            "fator_correcao": round(fator_correcao, 4),
            "valor_corrigido": round(valor_corrigido, 2),
            "valor_correcao": round(valor_corrigido - valor, 2)
        }