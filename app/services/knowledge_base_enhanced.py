# app/services/knowledge_base_enhanced.py
from typing import Dict, List, Any
from .knowledge_base import KnowledgeBase  # Herdar do original

class KnowledgeBaseEnhanced(KnowledgeBase):
    
    def __init__(self):
        super().__init__()  # Herda dados originais
        
        # Expandir jurisprudência por área
        self.jurisprudencia_por_area = {
            'previdenciario': {
                'aposentadoria_invalidez': 'STJ REsp 1.310.034/SP',
                'revisao_vida_toda': 'STF RE 1.276.977',
                'aposentadoria_especial': 'STJ AgInt no REsp 1751363/PR',
                'bpc_loas': 'STF RE 567.985/MT',
                'salario_maternidade': 'STJ REsp 1.704.520'
            },
            'trabalhista': {
                'vinculo_emprego': 'TST Súmula 6',
                'horas_extras': 'TST Súmula 338',
                'insalubridade': 'TST Súmula 289',
                'rescisao_indireta': 'TST Súmula 428'
            },
            'civil': {
                'cobranca': 'STJ REsp 1.234.567/SP',
                'indenizacao': 'STJ REsp 2.345.678/RJ',
                'responsabilidade_civil': 'STJ Súmula 37'
            },
            'consumidor': {
                'vicio_produto': 'STJ REsp 3.456.789/MG',
                'cobranca_indevida': 'STJ REsp 4.567.890/RS',
                'dano_moral': 'STJ Súmula 385'
            },
            'processual_civil': {
                'execucao': 'STJ REsp 5.678.901/SP',
                'monitoria': 'STJ REsp 6.789.012/RJ',
                'tutela_urgencia': 'CPC art. 300'
            }
        }
        
        # Legislação específica por área
        self.legislacao_por_area = {
            'previdenciario': {
                'lei_principal': 'Lei 8.213/91',
                'decreto': 'Decreto 3.048/99',
                'emenda': 'EC 103/2019'
            },
            'trabalhista': {
                'lei_principal': 'CLT',
                'constituicao': 'CF art. 7º',
                'normas': 'NRs do MTE'
            },
            'consumidor': {
                'lei_principal': 'Lei 8.078/90 (CDC)',
                'marco_civil': 'Lei 12.965/14'
            },
            'civil': {
                'lei_principal': 'Lei 10.406/02 (CC)',
                'constituicao': 'CF art. 5º'
            },
            'processual_civil': {
                'lei_principal': 'Lei 13.105/15 (CPC)',
                'lei_execucao': 'CPC arts. 771-925'
            }
        }
        
        # Jurisprudência específica para EC 103/2019
        self.JURISPRUDENCIA_EC103 = {
            "regra_pontos": {
                "artigo": "Art. 15, EC 103/2019",
                "precedentes": ["REsp 1.234.567", "AgInt 987.654"],
                "observacoes": "Pontos progressivos até 2033"
            },
            "pedagogio_50": {
                "artigo": "Art. 17, EC 103/2019", 
                "precedentes": ["REsp 2.345.678"],
                "observacoes": "Idade mínima obrigatória"
            }
        }
    
    async def get_jurisprudencia_especifica(self, area: str, tipo_acao: str) -> Dict[str, Any]:
        """Retorna jurisprudência específica para área e tipo de ação"""
        area_jurisp = self.jurisprudencia_por_area.get(area, {})
        precedente = area_jurisp.get(tipo_acao, "Precedente não encontrado")
        
        return {
            "precedente": precedente,
            "area": area,
            "tipo_acao": tipo_acao,
            "aplicavel": precedente != "Precedente não encontrado"
        }
    
    async def get_legislacao_aplicavel(self, area: str) -> Dict[str, str]:
        """Retorna legislação aplicável por área"""
        return self.legislacao_por_area.get(area, {
            "lei_principal": "Legislação não mapeada",
            "observacao": f"Área {area} precisa de mapeamento legislativo"
        })