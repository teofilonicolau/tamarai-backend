# app/core/calculators/familia_calculator.py

from typing import Dict, Any

class CalculadoraFamilia:
    
    def calcular_pensao_alimenticia(self, renda_alimentante: float, 
                                   numero_filhos: int, 
                                   percentual_sugerido: float = 0.30) -> Dict[str, Any]:
        """Calcula pensão alimentícia"""
        
        renda_disponivel = renda_alimentante * 0.70
        valor_por_filho = (renda_disponivel * percentual_sugerido) / numero_filhos
        
        return {
            "renda_alimentante": renda_alimentante,
            "renda_disponivel": round(renda_disponivel, 2),
            "numero_filhos": numero_filhos,
            "percentual_aplicado": f"{percentual_sugerido * 100}%",
            "valor_por_filho": round(valor_por_filho, 2),
            "valor_total_pensao": round(valor_por_filho * numero_filhos, 2),
            "observacao": "Valor sugerido - sujeito à análise judicial"
        }
