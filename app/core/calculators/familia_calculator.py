# app/core/calculators/familia_calculator.py
# ...existing code...
from typing import Dict, Any

class CalculadoraFamilia:
    
    def calcular_pensao_alimenticia(self, renda_alimentante: float, 
                                   numero_filhos: int, 
                                   percentual_sugerido: float = 0.30) -> Dict[str, Any]:
        """Calcula pensão alimentícia com tratamento de casos limites (evita divisão por zero)."""

        observacao = []

        # Normalizar entradas
        try:
            renda_alimentante = float(renda_alimentante)
        except (ValueError, TypeError):
            renda_alimentante = 0.0

        try:
            numero_filhos = int(numero_filhos)
        except (ValueError, TypeError):
            numero_filhos = 0

        # Validar percentual sugerido
        try:
            percentual_sugerido = float(percentual_sugerido)
        except (ValueError, TypeError):
            percentual_sugerido = 0.30
            observacao.append("Percentual sugerido inválido, usando 30%")

        if not 0 <= percentual_sugerido <= 1:
            percentual_sugerido = 0.30  # Valor padrão se inválido
            observacao.append("Percentual sugerido fora do intervalo (0-1), usando 30%")

        # Casos inválidos / limites
        if renda_alimentante <= 0 or numero_filhos <= 0:
            if renda_alimentante <= 0:
                observacao.append("Renda alimentante deve ser maior que 0")
            if numero_filhos <= 0:
                observacao.append("Número de filhos deve ser maior que 0")
            return {
                "renda_alimentante": round(renda_alimentante, 2),
                "renda_disponivel": 0.0,
                "numero_filhos": numero_filhos,
                "percentual_aplicado": f"{round(percentual_sugerido * 100, 2)}%",
                "valor_por_filho": 0.0,
                "valor_total_pensao": 0.0,
                "observacao": " | ".join(observacao) or "Dados insuficientes para cálculo"
            }

        # Cálculo normal
        renda_disponivel = renda_alimentante * 0.70
        valor_por_filho = (renda_disponivel * percentual_sugerido) / numero_filhos
        valor_total = valor_por_filho * numero_filhos

        return {
            "renda_alimentante": round(renda_alimentante, 2),
            "renda_disponivel": round(renda_disponivel, 2),
            "numero_filhos": numero_filhos,
            "percentual_aplicado": f"{round(percentual_sugerido * 100, 2)}%",
            "valor_por_filho": round(valor_por_filho, 2),
            "valor_total_pensao": round(valor_total, 2),
            "observacao": " | ".join(observacao) or "Valor sugerido - sujeito à análise judicial"
        }
# ...existing code...
