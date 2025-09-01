# app/core/calculators/trabalhista_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, Optional, List  # ← ADICIONAR List aqui
import math

class CalculadoraTrabalhista:
    
    def calcular_horas_extras(self, jornada_contratual: int, jornada_real: int, 
                             dias_trabalhados: int, valor_hora: float) -> Dict[str, Any]:
        """Calcula horas extras trabalhistas"""
        if jornada_real <= jornada_contratual:
            return {
                "horas_extras_diarias": 0,
                "valor_total": 0,
                "observacao": "Não há horas extras"
            }
        
        horas_extras_diarias = jornada_real - jornada_contratual
        total_horas_extras = horas_extras_diarias * dias_trabalhados
        
        # Adicional de 50% sobre as horas extras
        valor_hora_extra = valor_hora * 1.5
        valor_total = total_horas_extras * valor_hora_extra
        
        return {
            "horas_extras_diarias": horas_extras_diarias,
            "total_horas_extras": total_horas_extras,
            "valor_hora_normal": valor_hora,
            "valor_hora_extra": valor_hora_extra,
            "valor_total": round(valor_total, 2),
            "adicional_aplicado": "50%"
        }
    
    def calcular_adicional_insalubridade(self, salario_base: float, grau: str) -> Dict[str, Any]:
        """Calcula adicional de insalubridade"""
        percentuais = {
            "minimo": 0.10,    # 10%
            "medio": 0.20,     # 20%
            "maximo": 0.40     # 40%
        }
        
        percentual = percentuais.get(grau.lower(), 0.20)
        
        # Base de cálculo: salário mínimo (não o salário do empregado)
        salario_minimo = 1320.00  # Valor 2024 - deveria vir de configuração
        valor_adicional = salario_minimo * percentual
        
        return {
            "grau_insalubridade": grau,
            "percentual": f"{percentual * 100}%",
            "base_calculo": salario_minimo,
            "valor_mensal": round(valor_adicional, 2),
            "observacao": f"Adicional de {percentual * 100}% sobre salário mínimo"
        }
    
    def calcular_fgts_multa(self, salarios_periodo: List[float], tipo_rescisao: str) -> Dict[str, Any]:
        """Calcula FGTS e multa rescisória"""
        total_salarios = sum(salarios_periodo)
        fgts_8_porcento = total_salarios * 0.08
        
        # Multa varia conforme tipo de rescisão
        if tipo_rescisao == "sem_justa_causa":
            multa_percentual = 0.40  # 40%
        elif tipo_rescisao == "rescisao_indireta":
            multa_percentual = 0.40  # 40%
        else:
            multa_percentual = 0.00  # Sem multa
        
        valor_multa = fgts_8_porcento * multa_percentual
        
        return {
            "total_salarios_periodo": round(total_salarios, 2),
            "fgts_8_porcento": round(fgts_8_porcento, 2),
            "tipo_rescisao": tipo_rescisao,
            "percentual_multa": f"{multa_percentual * 100}%",
            "valor_multa": round(valor_multa, 2),
            "total_fgts_multa": round(fgts_8_porcento + valor_multa, 2)
        }