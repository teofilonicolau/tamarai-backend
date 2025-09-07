# app/core/calculators/processual_calculator.py

from datetime import date
from typing import Dict, Any

class CalculadoraProcessual:
    
    def _aplicar_correcao_ipca(self, valor: float, data_inicial: date) -> float:
        """Corrigir para evitar valores negativos"""
        if data_inicial >= date.today():
            return 0.0  # Sem correção se data futura
        
        anos_decorridos = max(0, (date.today() - data_inicial).days / 365)
        taxa_ipca_anual = 0.045
        fator_correcao = (1 + taxa_ipca_anual) ** anos_decorridos
        return valor * (fator_correcao - 1)

    def _calcular_juros_mora(self, valor: float, data_inicial: date) -> float:
        """Corrigir para evitar valores negativos"""
        if data_inicial >= date.today():
            return 0.0  # Sem juros se data futura
        
        meses_decorridos = max(0, (date.today() - data_inicial).days / 30)
        return valor * 0.01 * meses_decorridos

    def calcular_liquidacao_sentenca(self, valor_principal: float,
                                     data_sentenca: date,
                                     incluir_honorarios: bool = True) -> Dict[str, Any]:
        """Calcula liquidação completa de sentença"""
        
        correcao = self._aplicar_correcao_ipca(valor_principal, data_sentenca)
        juros = self._calcular_juros_mora(valor_principal, data_sentenca)
        
        valor_corrigido = valor_principal + correcao
        honorarios = valor_corrigido * 0.10 if incluir_honorarios else 0
        
        valor_total = valor_principal + correcao + juros + honorarios
        
        return {
            "valor_principal": valor_principal,
            "correcao_monetaria": round(correcao, 2),
            "juros_mora": round(juros, 2),
            "honorarios_advocaticios": round(honorarios, 2),
            "valor_total_liquidacao": round(valor_total, 2),
            "data_calculo": date.today().isoformat()
        }