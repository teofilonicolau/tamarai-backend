# app/services/feedback_service.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class FeedbackService:
    
    def __init__(self):
        self.feedback_data = []
    
    async def registrar_correcao(self, peticao_id: int, correcoes: dict) -> bool:
        """Registra correções feitas por advogados"""
        try:
            feedback_entry = {
                "peticao_id": peticao_id,
                "timestamp": datetime.now().isoformat(),
                "correcoes": correcoes,
                "tipo": "correcao_humana"
            }
            
            self.feedback_data.append(feedback_entry)
            
            # Aqui você salvaria no banco de dados
            # await self.salvar_no_banco(feedback_entry)
            
            return True
        except Exception as e:
            print(f"Erro ao registrar correção: {e}")
            return False
    
    async def treinar_modelo(self, feedback_data: list) -> dict:
        """Treina modelo com base no feedback"""
        try:
            # Analisar padrões de correção
            padroes = self._analisar_padroes_correcao(feedback_data)
            
            # Aqui você implementaria o fine-tuning
            # resultado_treinamento = await self._executar_fine_tuning(padroes)
            
            return {
                "status": "sucesso",
                "padroes_identificados": len(padroes),
                "melhorias_sugeridas": padroes[:5]  # Top 5
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e)
            }
    
    async def gerar_relatorio_qualidade(self) -> dict:
        """Gera relatório de qualidade das petições"""
        try:
            total_peticoes = len(self.feedback_data)
            
            if total_peticoes == 0:
                return {
                    "total_peticoes": 0,
                    "taxa_aprovacao": 0,
                    "principais_erros": [],
                    "recomendacoes": ["Aguardando mais dados para análise"]
                }
            
            # Calcular métricas
            correcoes_por_tipo = {}
            for feedback in self.feedback_data:
                for correcao in feedback.get("correcoes", {}):
                    tipo = correcao.get("tipo", "outros")
                    correcoes_por_tipo[tipo] = correcoes_por_tipo.get(tipo, 0) + 1
            
            return {
                "total_peticoes": total_peticoes,
                "taxa_aprovacao": self._calcular_taxa_aprovacao(),
                "principais_erros": list(correcoes_por_tipo.keys())[:5],
                "correcoes_por_tipo": correcoes_por_tipo,
                "recomendacoes": self._gerar_recomendacoes(correcoes_por_tipo)
            }
        except Exception as e:
            return {
                "erro": str(e),
                "status": "erro_no_relatorio"
            }
    
    def _analisar_padroes_correcao(self, feedback_data: list) -> list:
        """Analisa padrões nas correções"""
        padroes = []
        
        for feedback in feedback_data:
            for correcao in feedback.get("correcoes", []):
                padrao = {
                    "tipo_erro": correcao.get("tipo", "indefinido"),
                    "frequencia": 1,
                    "sugestao_melhoria": correcao.get("sugestao", "")
                }
                padroes.append(padrao)
        
        return padroes
    
    def _calcular_taxa_aprovacao(self) -> float:
        """Calcula taxa de aprovação das petições"""
        if not self.feedback_data:
            return 0.0
        
        aprovadas = sum(1 for f in self.feedback_data 
                       if f.get("aprovado", False))
        
        return round((aprovadas / len(self.feedback_data)) * 100, 2)
    
    def _gerar_recomendacoes(self, correcoes_por_tipo: dict) -> list:
        """Gera recomendações baseadas nos erros mais comuns"""
        recomendacoes = []
        
        for tipo_erro, frequencia in sorted(correcoes_por_tipo.items(), 
                                          key=lambda x: x[1], reverse=True)[:3]:
            if tipo_erro == "data_inconsistente":
                recomendacoes.append("Implementar validação automática de datas")
            elif tipo_erro == "calculo_incorreto":
                recomendacoes.append("Melhorar calculadora previdenciária")
            elif tipo_erro == "jurisprudencia_generica":
                recomendacoes.append("Expandir base de jurisprudência específica")
            else:
                recomendacoes.append(f"Revisar processo para: {tipo_erro}")
        
        return recomendacoes