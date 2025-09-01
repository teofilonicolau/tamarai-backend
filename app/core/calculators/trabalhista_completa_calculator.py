# app/core/calculators/trabalhista_completa_calculator.py
from datetime import date, timedelta
from typing import Dict, Any, List
from .trabalhista_calculator import CalculadoraTrabalhista

class CalculadoraTrabalhistaCompleta(CalculadoraTrabalhista):
    """Extensão modular para cálculos trabalhistas completos"""
    
    def calcular_verbas_rescisorias_completas(self, dados_rescisao: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula todas as verbas rescisórias"""
        
        # Dados básicos
        salario = dados_rescisao.get("salario", 0)
        data_admissao = dados_rescisao.get("data_admissao")
        data_rescisao = dados_rescisao.get("data_rescisao")
        tipo_rescisao = dados_rescisao.get("tipo_rescisao", "sem_justa_causa")
        
        # Calcular tempo de serviço
        tempo_servico = self._calcular_tempo_servico(data_admissao, data_rescisao)
        
        verbas = {}
        
        # 1. Saldo de salário
        verbas["saldo_salario"] = self._calcular_saldo_salario(salario, data_rescisao)
        
        # 2. Aviso prévio
        verbas["aviso_previo"] = self._calcular_aviso_previo(salario, tempo_servico, tipo_rescisao)
        
        # 3. 13º salário proporcional
        verbas["decimo_terceiro"] = self._calcular_decimo_terceiro(salario, data_rescisao)
        
        # 4. Férias proporcionais + 1/3
        verbas["ferias"] = self._calcular_ferias_proporcionais(salario, data_admissao, data_rescisao)
        
        # 5. FGTS + multa
        verbas["fgts"] = self.calcular_fgts_multa([salario] * tempo_servico["meses"], tipo_rescisao)
        
        # 6. Seguro-desemprego (se aplicável)
        verbas["seguro_desemprego"] = self._calcular_seguro_desemprego(tempo_servico, tipo_rescisao)
        
        # Total geral
        total_verbas = sum(verba.get("valor_total", 0) for verba in verbas.values() 
                          if isinstance(verba, dict))
        
        return {
            "verbas_detalhadas": verbas,
            "tempo_servico": tempo_servico,
            "total_verbas_rescisorias": round(total_verbas, 2),
            "tipo_rescisao": tipo_rescisao
        }
    
    def _calcular_aviso_previo(self, salario: float, tempo_servico: Dict, tipo_rescisao: str) -> Dict[str, Any]:
        """Calcula aviso prévio indenizado"""
        if tipo_rescisao not in ["sem_justa_causa", "rescisao_indireta"]:
            return {"valor_total": 0, "observacao": "Não há direito a aviso prévio"}
        
        # 30 dias + 3 dias por ano trabalhado (máximo 90 dias)
        anos_trabalhados = tempo_servico["anos"]
        dias_aviso = min(30 + (anos_trabalhados * 3), 90)
        valor_aviso = (salario / 30) * dias_aviso
        
        return {
            "dias_aviso": dias_aviso,
            "valor_diario": round(salario / 30, 2),
            "valor_total": round(valor_aviso, 2),
            "observacao": f"Aviso prévio de {dias_aviso} dias"
        }
    
    def _calcular_ferias_proporcionais(self, salario: float, data_admissao: date, data_rescisao: date) -> Dict[str, Any]:
        """Calcula férias proporcionais + 1/3 constitucional"""
        # Calcular meses trabalhados no período aquisitivo atual
        ultimo_periodo_ferias = data_admissao  # Simplificado
        meses_periodo_atual = (data_rescisao - ultimo_periodo_ferias).days // 30
        
        # Férias proporcionais (1/12 por mês trabalhado)
        ferias_proporcionais = (salario / 12) * meses_periodo_atual
        
        # 1/3 constitucional
        um_terco = ferias_proporcionais / 3
        
        total_ferias = ferias_proporcionais + um_terco
        
        return {
            "meses_periodo_atual": meses_periodo_atual,
            "ferias_proporcionais": round(ferias_proporcionais, 2),
            "um_terco_constitucional": round(um_terco, 2),
            "valor_total": round(total_ferias, 2),
            "observacao": f"Férias de {meses_periodo_atual}/12 + 1/3"
        }