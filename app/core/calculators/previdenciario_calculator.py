# app/core/calculators/previdenciario_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, Optional
import math

class CalculadoraPrevidenciaria:
    
    def converter_anos_meses(self, valor: int, unidade: str) -> int:
        """27 anos = 324 meses, não 27 meses"""
        if unidade.lower() in ['ano', 'anos', 'year', 'years']:
            return valor * 12
        elif unidade.lower() in ['mes', 'meses', 'month', 'months']:
            return valor
        else:
            # Se não especificado e valor > 50, provavelmente já é meses
            return valor if valor > 50 else valor * 12
        
    def calcular_periodo_graca(self, tipo_segurado: str, ultima_contribuicao: date) -> dict:
        """Segurado comum: 12 meses, Rural: sem período de graça"""
        hoje = date.today()
        diferenca = hoje - ultima_contribuicao
        
        if tipo_segurado == "rural_pura":
            # Segurado especial não tem período de graça
            return {
                "tem_periodo_graca": True,
                "dias_sem_contribuir": diferenca.days,
                "periodo_graca_valido": True,
                "observacao": "Segurado especial não perde qualidade"
            }
        else:
            # Segurado comum: 12 meses de período de graça
            periodo_graca_dias = 365
            periodo_valido = diferenca.days <= periodo_graca_dias
            
            return {
                "tem_periodo_graca": True,
                "dias_sem_contribuir": diferenca.days,
                "periodo_graca_valido": periodo_valido,
                "dias_restantes": max(0, periodo_graca_dias - diferenca.days),
                "observacao": f"Período de graça: {'válido' if periodo_valido else 'expirado'}"
            }
        
    def somar_tempos_contributivos(self, rural: int, urbano: int, especial: int) -> dict:
        """Conversão com fatores corretos"""
        # Converter tempo especial (fator 1.4 para homem, 1.2 para mulher)
        especial_convertido_homem = math.floor(especial * 1.4)
        especial_convertido_mulher = math.floor(especial * 1.2)
        
        return {
            "tempo_rural_meses": rural,
            "tempo_urbano_meses": urbano,
            "tempo_especial_meses": especial,
            "tempo_especial_convertido_homem": especial_convertido_homem,
            "tempo_especial_convertido_mulher": especial_convertido_mulher,
            "total_homem": rural + urbano + especial_convertido_homem,
            "total_mulher": rural + urbano + especial_convertido_mulher,
            "total_anos_homem": (rural + urbano + especial_convertido_homem) // 12,
            "total_anos_mulher": (rural + urbano + especial_convertido_mulher) // 12
        }
        
    def calcular_valor_causa(self, parcelas_vencidas: int, valor_mensal: float) -> float:
        """Cálculo automático para petições"""
        if parcelas_vencidas <= 0 or valor_mensal <= 0:
            return 1000.0  # Valor mínimo padrão
        
        valor_total = parcelas_vencidas * valor_mensal
        
        # Adicionar 12 parcelas vincendas como estimativa
        valor_total += 12 * valor_mensal
        
        return round(valor_total, 2)
    
    def validar_carencia_por_beneficio(self, tipo_beneficio: str, contribuicoes: int) -> dict:
        """Valida carência específica por tipo de benefício"""
        carencias = {
            "aposentadoria_invalidez": 12,
            "aposentadoria_idade": 180,
            "aposentadoria_tempo": 180,
            "auxilio_doenca": 12,
            "salario_maternidade": 10,
            "pensao_morte": 0,  # Sem carência
            "bpc_loas": 0  # Sem carência
        }
        
        carencia_necessaria = carencias.get(tipo_beneficio, 12)
        carencia_cumprida = contribuicoes >= carencia_necessaria
        
        return {
            "carencia_necessaria": carencia_necessaria,
            "contribuicoes_atuais": contribuicoes,
            "carencia_cumprida": carencia_cumprida,
            "contribuicoes_faltantes": max(0, carencia_necessaria - contribuicoes)
        }