# app/core/calculators/previdenciario_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, Optional, List
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
    
    def formatar_tempo_anos_meses(self, meses_totais: int) -> str:
        """Converte meses para formato 'X anos e Y meses'"""
        anos = meses_totais // 12
        meses = meses_totais % 12
        
        if anos == 0:
            return f"{meses} meses"
        elif meses == 0:
            return f"{anos} anos"
        else:
            return f"{anos} anos e {meses} meses"
    
    def validar_limites_tempo_especial(self, tempo_especial: int, data_inicio: Optional[date] = None) -> Dict[str, Any]:
        """Valida limites legais para tempo especial"""
        alertas = []
        
        # Limite máximo: 25 anos (300 meses)
        if tempo_especial > 300:
            alertas.append("Tempo especial superior a 25 anos - verificar documentação")
        
        # Verificar se data de início é anterior a 1991 (Lei 8.213/91)
        if data_inicio and data_inicio < date(1991, 7, 24):
            alertas.append("Atividade anterior à Lei 8.213/91 - aplicar legislação específica")
        
        # Verificar se não é data futura
        if data_inicio and data_inicio > date.today():
            alertas.append("Data de início não pode ser futura")
        
        return {
            "tempo_valido": tempo_especial <= 300 and (not data_inicio or data_inicio <= date.today()),
            "alertas": alertas,
            "limite_maximo_meses": 300,
            "limite_maximo_anos": 25
        }
        
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
        
    def somar_tempos_contributivos(self, rural: int, urbano: int, especial: int, 
                                 data_inicio_especial: Optional[date] = None) -> dict:
        """Conversão com fatores corretos + melhorias"""
        
        # Validar limites
        validacao = self.validar_limites_tempo_especial(especial, data_inicio_especial)
        
        # Converter tempo especial (fator 1.4 para homem, 1.2 para mulher)
        especial_convertido_homem = math.floor(especial * 1.4)
        especial_convertido_mulher = math.floor(especial * 1.2)
        
        # Totais
        total_homem = rural + urbano + especial_convertido_homem
        total_mulher = rural + urbano + especial_convertido_mulher
        
        resultado = {
            "tempo_rural_meses": rural,
            "tempo_urbano_meses": urbano,
            "tempo_especial_meses": especial,
            "tempo_especial_convertido_homem": especial_convertido_homem,
            "tempo_especial_convertido_mulher": especial_convertido_mulher,
            "total_homem": total_homem,
            "total_mulher": total_mulher,
            "total_anos_homem": total_homem // 12,
            "total_anos_mulher": total_mulher // 12,
            "total_formatado_homem": self.formatar_tempo_anos_meses(total_homem),
            "total_formatado_mulher": self.formatar_tempo_anos_meses(total_mulher),
            "tempo_especial_formatado": self.formatar_tempo_anos_meses(especial),
            "validacao": validacao
        }
        
        # Adicionar data de início se fornecida
        if data_inicio_especial:
            resultado["data_inicio_atividade_especial"] = data_inicio_especial.isoformat()
            
            # Calcular período de exposição
            data_fim = date.today()  # Ou data específica se fornecida
            periodo_exposicao = (data_fim - data_inicio_especial).days // 30  # Em meses
            resultado["periodo_exposicao_meses"] = periodo_exposicao
            resultado["periodo_exposicao_formatado"] = self.formatar_tempo_anos_meses(periodo_exposicao)
        
        return resultado
        
    def calcular_valor_causa(self, parcelas_vencidas: int, valor_mensal: float) -> float:
        """
        Calcular valor da causa para ações previdenciárias
        
        Args:
            parcelas_vencidas: Número de parcelas em atraso
            valor_mensal: Valor mensal do benefício
        
        Returns:
            float: Valor da causa (parcelas vencidas + 12 parcelas futuras)
        """
        # Valor das parcelas vencidas
        valor_vencidas = parcelas_vencidas * valor_mensal
        
        # Valor de 12 parcelas futuras (padrão jurisprudencial)
        valor_futuras = 12 * valor_mensal
        
        # Valor total da causa
        valor_total = valor_vencidas + valor_futuras
        
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
    
    def calcular_revisao_vida_toda(self, salarios_antes_1994: List[float],
                                 salarios_depois_1994: List[float],
                                 data_dib: date) -> Dict[str, Any]:
        """Calcula revisão da vida toda"""
        
        # Média com todos os salários (vida toda)
        todos_salarios = salarios_antes_1994 + salarios_depois_1994
        media_vida_toda = sum(todos_salarios) / len(todos_salarios) if todos_salarios else 0.0
        
        # Média apenas pós-1994 (regra atual)
        media_pos_1994 = sum(salarios_depois_1994) / len(salarios_depois_1994) if salarios_depois_1994 else 0.0
        
        # Diferença
        diferenca_mensal = media_vida_toda - media_pos_1994
        
        # Calcular meses desde DIB
        meses_desde_dib = (date.today() - data_dib).days // 30
        
        valor_devido = diferenca_mensal * meses_desde_dib
        
        return {
            "media_vida_toda": round(media_vida_toda, 2),
            "media_pos_1994": round(media_pos_1994, 2),
            "diferenca_mensal": round(diferenca_mensal, 2),
            "meses_desde_dib": meses_desde_dib,
            "valor_devido_bruto": round(valor_devido, 2),
            "vantajosa": diferenca_mensal > 0,
            "observacao": "Sujeito à análise de viabilidade jurídica"
        }