# app/core/calculators/previdenciario_ec103_calculator.py
from datetime import date
from typing import Dict, Any, Optional
from .previdenciario_calculator import CalculadoraPrevidenciaria

class CalculadoraPrevidenciariaEC103(CalculadoraPrevidenciaria):
    """Extensão modular para regras da EC 103/2019"""
    
    def __init__(self):
        super().__init__()
        self.data_ec103 = date(2019, 11, 13)  # Data da EC 103
    
    def calcular_regra_transicao(self, sexo: str, idade_atual: int, 
                                tempo_contribuicao_atual: int, 
                                tempo_contribuicao_em_13_11_2019: int) -> Dict[str, Any]:
        """Calcula melhor regra de transição da EC 103"""
        
        regras_disponiveis = []
        
        # 1. PEDÁGIO 50%
        pedagogio_50 = self._calcular_pedagogio_50(
            sexo, idade_atual, tempo_contribuicao_atual, tempo_contribuicao_em_13_11_2019
        )
        if pedagogio_50["elegivel"]:
            regras_disponiveis.append(pedagogio_50)
        
        # 2. PEDÁGIO 100%
        pedagogio_100 = self._calcular_pedagogio_100(
            sexo, idade_atual, tempo_contribuicao_atual, tempo_contribuicao_em_13_11_2019
        )
        if pedagogio_100["elegivel"]:
            regras_disponiveis.append(pedagogio_100)
        
        # 3. REGRA GERAL EC 103
        regra_geral = self._calcular_regra_geral_ec103(
            sexo, idade_atual, tempo_contribuicao_atual
        )
        if regra_geral["elegivel"]:
            regras_disponiveis.append(regra_geral)
        
        # 4. REGRA DE PONTOS
        regra_pontos = self._calcular_regra_pontos(
            sexo, idade_atual, tempo_contribuicao_atual
        )
        if regra_pontos["elegivel"]:
            regras_disponiveis.append(regra_pontos)
        
        # Escolher a melhor regra (menor tempo faltante)
        melhor_regra = min(regras_disponiveis, 
                          key=lambda x: x["meses_faltantes"], 
                          default={"regra": "nenhuma_elegivel"})
        
        return {
            "melhor_regra": melhor_regra,
            "todas_regras": regras_disponiveis,
            "total_regras_elegiveis": len(regras_disponiveis)
        }
    
    def _calcular_pedagogio_50(self, sexo: str, idade_atual: int, 
                              tempo_atual: int, tempo_em_13_11_2019: int) -> Dict[str, Any]:
        """Pedágio 50% - Art. 17 da EC 103"""
        tempo_necessario = 420 if sexo.lower() == "masculino" else 360  # 35/30 anos
        idade_minima = 61 if sexo.lower() == "masculino" else 56
        
        tempo_faltante_em_2019 = max(0, tempo_necessario - tempo_em_13_11_2019)
        pedagogio = tempo_faltante_em_2019 * 0.5  # 50% do tempo faltante
        
        tempo_total_necessario = tempo_necessario + pedagogio
        tempo_ainda_faltante = max(0, tempo_total_necessario - tempo_atual)
        
        elegivel = (tempo_em_13_11_2019 > 0 and 
                   idade_atual >= idade_minima and 
                   tempo_atual >= tempo_total_necessario)
        
        return {
            "regra": "pedagogio_50",
            "elegivel": elegivel,
            "idade_minima": idade_minima,
            "tempo_necessario": tempo_total_necessario,
            "tempo_atual": tempo_atual,
            "meses_faltantes": tempo_ainda_faltante,
            "pedagogio_meses": pedagogio,
            "observacao": f"Pedágio de {pedagogio} meses sobre tempo faltante em 2019"
        }
    
    def _calcular_pedagogio_100(self, sexo: str, idade_atual: int, 
                               tempo_atual: int, tempo_em_13_11_2019: int) -> Dict[str, Any]:
        """Pedágio 100% - Art. 20 da EC 103"""
        tempo_necessario = 420 if sexo.lower() == "masculino" else 360  # 35/30 anos
        idade_minima = 60 if sexo.lower() == "masculino" else 57
        
        tempo_faltante_em_2019 = max(0, tempo_necessario - tempo_em_13_11_2019)
        pedagogio = tempo_faltante_em_2019  # 100% do tempo faltante
        
        tempo_total_necessario = tempo_necessario + pedagogio
        tempo_ainda_faltante = max(0, tempo_total_necessario - tempo_atual)
        
        elegivel = (tempo_em_13_11_2019 > 0 and 
                   idade_atual >= idade_minima and 
                   tempo_atual >= tempo_total_necessario)
        
        return {
            "regra": "pedagogio_100",
            "elegivel": elegivel,
            "idade_minima": idade_minima,
            "tempo_necessario": tempo_total_necessario,
            "tempo_atual": tempo_atual,
            "meses_faltantes": tempo_ainda_faltante,
            "pedagogio_meses": pedagogio,
            "observacao": f"Pedágio de {pedagogio} meses (100% do tempo faltante em 2019)"
        }
    
    def _calcular_regra_geral_ec103(self, sexo: str, idade_atual: int, 
                                   tempo_atual: int) -> Dict[str, Any]:
        """Regra Geral EC 103 - Art. 19"""
        idade_minima = 65 if sexo.lower() == "masculino" else 62
        tempo_minimo = 240 if sexo.lower() == "masculino" else 180  # 20/15 anos
        
        elegivel = idade_atual >= idade_minima and tempo_atual >= tempo_minimo
        
        return {
            "regra": "regra_geral_ec103",
            "elegivel": elegivel,
            "idade_minima": idade_minima,
            "tempo_minimo": tempo_minimo,
            "idade_atual": idade_atual,
            "tempo_atual": tempo_atual,
            "meses_faltantes": max(0, tempo_minimo - tempo_atual),
            "observacao": "Regra geral da EC 103 - idade + tempo mínimo"
        }
    
    def _calcular_regra_pontos(self, sexo: str, idade_atual: int, 
                              tempo_atual: int) -> Dict[str, Any]:
        """Regra de Pontos - Art. 16 da EC 103"""
        tempo_minimo = 420 if sexo.lower() == "masculino" else 360  # 35/30 anos
        
        # Pontos necessários (progressivos até 2033)
        ano_atual = date.today().year
        pontos_base = 96 if sexo.lower() == "masculino" else 86
        anos_desde_2019 = max(0, ano_atual - 2019)
        pontos_necessarios = pontos_base + anos_desde_2019
        pontos_maximos = 105 if sexo.lower() == "masculino" else 100
        
        pontos_necessarios = min(pontos_necessarios, pontos_maximos)
        pontos_atuais = idade_atual + (tempo_atual // 12)
        
        elegivel = (tempo_atual >= tempo_minimo and 
                   pontos_atuais >= pontos_necessarios)
        
        return {
            "regra": "regra_pontos",
            "elegivel": elegivel,
            "tempo_minimo": tempo_minimo,
            "pontos_necessarios": pontos_necessarios,
            "pontos_atuais": pontos_atuais,
            "pontos_faltantes": max(0, pontos_necessarios - pontos_atuais),
            "meses_faltantes": max(0, tempo_minimo - tempo_atual),
            "observacao": f"Regra de pontos: {pontos_atuais}/{pontos_necessarios} pontos"
        }