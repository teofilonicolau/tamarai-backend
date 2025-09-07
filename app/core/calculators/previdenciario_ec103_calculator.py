# app/core/calculators/previdenciario_ec103_calculator.py

from datetime import date
from typing import Dict, Any
import math

class CalculadoraPrevidenciariaEC103:
    
    def calcular_regra_transicao(self, sexo: str, idade_atual: int, 
                                tempo_contribuicao_atual: int,
                                tempo_contribuicao_em_13_11_2019: int) -> Dict[str, Any]:
        """
        Calcula todas as regras de transição da EC 103/2019
        """
        todas_regras = []
        regras_elegiveis = []
        
        # 1. REGRA DE PONTOS (Art. 15) - SEM PEDÁGIO
        pontos_regra = self._calcular_regra_pontos(sexo, idade_atual, tempo_contribuicao_atual)
        todas_regras.append(pontos_regra)
        if pontos_regra["elegivel"]:
            regras_elegiveis.append(pontos_regra)
        
        # 2. REGRA GERAL (Art. 19) - SEM PEDÁGIO
        geral_regra = self._calcular_regra_geral(sexo, idade_atual, tempo_contribuicao_atual)
        todas_regras.append(geral_regra)
        if geral_regra["elegivel"]:
            regras_elegiveis.append(geral_regra)
        
        # 3. PEDÁGIO 50% (Art. 17)
        pedagogio_50_regra = self._calcular_pedagogio_50(
            sexo, idade_atual, tempo_contribuicao_atual, tempo_contribuicao_em_13_11_2019
        )
        todas_regras.append(pedagogio_50_regra)
        if pedagogio_50_regra["elegivel"]:
            regras_elegiveis.append(pedagogio_50_regra)
        
        # 4. PEDÁGIO 100% (Art. 20)
        pedagogio_100_regra = self._calcular_pedagogio_100(
            sexo, idade_atual, tempo_contribuicao_atual, tempo_contribuicao_em_13_11_2019
        )
        todas_regras.append(pedagogio_100_regra)
        if pedagogio_100_regra["elegivel"]:
            regras_elegiveis.append(pedagogio_100_regra)
        
        # Encontrar melhor regra (elegível ou mais próxima)
        melhor_regra = self._encontrar_melhor_regra(todas_regras)
        
        return {
            "melhor_regra": melhor_regra,
            "todas_regras": todas_regras,
            "regras_elegiveis": regras_elegiveis,
            "total_regras_elegiveis": len(regras_elegiveis),
            "total_regras_analisadas": len(todas_regras)
        }
    
    def _calcular_regra_pontos(self, sexo: str, idade: int, tempo_contrib: int) -> Dict[str, Any]:
        """Regra de Pontos - Art. 15 EC 103/2019"""
        pontos_atuais = idade + tempo_contrib
        
        # Pontos exigidos por ano
        pontos_2025 = 99 if sexo.lower() == "masculino" else 89
        
        elegivel = pontos_atuais >= pontos_2025
        pontos_faltantes = max(0, pontos_2025 - pontos_atuais)
        
        return {
            "regra": "regra_pontos",
            "nome": "Regra de Pontos (Art. 15)",
            "elegivel": elegivel,
            "pontos_atuais": pontos_atuais,
            "pontos_exigidos": pontos_2025,
            "pontos_faltantes": pontos_faltantes,
            "tempo_minimo": 35 if sexo.lower() == "masculino" else 30,
            "tempo_atual": tempo_contrib,
            "observacao": "Sem idade mínima, apenas pontos + tempo mínimo"
        }
    
    def _calcular_regra_geral(self, sexo: str, idade: int, tempo_contrib: int) -> Dict[str, Any]:
        """Regra Geral - Art. 19 EC 103/2019"""
        idade_minima = 65 if sexo.lower() == "masculino" else 62
        tempo_minimo = 20  # Homem e mulher
        
        elegivel = idade >= idade_minima and tempo_contrib >= tempo_minimo
        idade_faltante = max(0, idade_minima - idade)
        tempo_faltante = max(0, tempo_minimo - tempo_contrib)
        
        return {
            "regra": "regra_geral",
            "nome": "Regra Geral (Art. 19)",
            "elegivel": elegivel,
            "idade_atual": idade,
            "idade_minima": idade_minima,
            "idade_faltante": idade_faltante,
            "tempo_atual": tempo_contrib,
            "tempo_minimo": tempo_minimo,
            "tempo_faltante": tempo_faltante,
            "observacao": "Idade mínima + 20 anos de contribuição"
        }
    
    def _calcular_pedagogio_50(self, sexo: str, idade: int, tempo_contrib: int, 
                              tempo_em_13_11_2019: int) -> Dict[str, Any]:
        """Pedágio 50% - Art. 17 EC 103/2019"""
        idade_minima = 65 if sexo.lower() == "masculino" else 62
        tempo_minimo_antigo = 35 if sexo.lower() == "masculino" else 30
        
        # Tempo que faltava em 13/11/2019
        tempo_faltante_2019 = max(0, tempo_minimo_antigo - tempo_em_13_11_2019)
        
        # Pedágio de 50%
        pedagogio = math.ceil(tempo_faltante_2019 * 0.5)
        
        # Tempo total necessário
        tempo_total_necessario = tempo_minimo_antigo + pedagogio
        
        elegivel = (idade >= idade_minima and 
                   tempo_contrib >= tempo_total_necessario and
                   tempo_em_13_11_2019 > 0)
        
        return {
            "regra": "pedagogio_50",
            "nome": "Pedágio 50% (Art. 17)",
            "elegivel": elegivel,
            "idade_atual": idade,
            "idade_minima": idade_minima,
            "tempo_atual": tempo_contrib,
            "tempo_em_2019": tempo_em_13_11_2019,
            "tempo_faltante_2019": tempo_faltante_2019,
            "pedagogio_meses": pedagogio,
            "tempo_total_necessario": tempo_total_necessario,
            "tempo_ainda_faltante": max(0, tempo_total_necessario - tempo_contrib),
            "observacao": f"Pedágio de {pedagogio} meses sobre tempo faltante em 2019"
        }
    
    def _calcular_pedagogio_100(self, sexo: str, idade: int, tempo_contrib: int,
                               tempo_em_13_11_2019: int) -> Dict[str, Any]:
        """Pedágio 100% - Art. 20 EC 103/2019"""
        idade_minima = 60 if sexo.lower() == "masculino" else 57
        tempo_minimo_antigo = 35 if sexo.lower() == "masculino" else 30
        
        # Tempo que faltava em 13/11/2019
        tempo_faltante_2019 = max(0, tempo_minimo_antigo - tempo_em_13_11_2019)
        
        # Pedágio de 100%
        pedagogio = tempo_faltante_2019
        
        # Tempo total necessário
        tempo_total_necessario = tempo_minimo_antigo + pedagogio
        
        elegivel = (idade >= idade_minima and 
                   tempo_contrib >= tempo_total_necessario and
                   tempo_em_13_11_2019 > 0)
        
        return {
            "regra": "pedagogio_100",
            "nome": "Pedágio 100% (Art. 20)",
            "elegivel": elegivel,
            "idade_atual": idade,
            "idade_minima": idade_minima,
            "tempo_atual": tempo_contrib,
            "tempo_em_2019": tempo_em_13_11_2019,
            "tempo_faltante_2019": tempo_faltante_2019,
            "pedagogio_meses": pedagogio,
            "tempo_total_necessario": tempo_total_necessario,
            "tempo_ainda_faltante": max(0, tempo_total_necessario - tempo_contrib),
            "observacao": f"Pedágio de {pedagogio} meses (100% do faltante em 2019)"
        }
    
    def _encontrar_melhor_regra(self, todas_regras: list) -> Dict[str, Any]:
        """Encontra a melhor regra (elegível ou mais próxima)"""
        if not todas_regras:
            return {"regra": "nenhuma_regra_encontrada"}
        
        # Primeiro, tentar encontrar regras elegíveis
        elegiveis = [r for r in todas_regras if r.get("elegivel", False)]
        
        if elegiveis:
            # Se há elegíveis, pegar a melhor
            melhor = min(elegiveis, 
                        key=lambda x: x.get("tempo_ainda_faltante", 0) + 
                                     x.get("idade_faltante", 0) + 
                                     x.get("pontos_faltantes", 0))
            return melhor
        else:
            # Se nenhuma elegível, pegar a mais próxima
            melhor = min(todas_regras, 
                        key=lambda x: x.get("tempo_ainda_faltante", 999) + 
                                     x.get("idade_faltante", 999) + 
                                     x.get("pontos_faltantes", 999))
            
            # Adicionar flag indicando que não está elegível ainda
            melhor_copia = melhor.copy()
            melhor_copia["status"] = "mais_proxima"
            melhor_copia["observacao_adicional"] = "Regra mais próxima de ser atingida"
            
            return melhor_copia