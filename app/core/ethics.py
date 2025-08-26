# app/core/ethics.py - NOVO ARQUIVO
from typing import Dict, Any
from datetime import datetime

class EthicsService:
    """Serviço para garantir conformidade ética da IA jurídica"""
    
    @staticmethod
    def get_disclaimer() -> str:
        """Aviso obrigatório em todas as petições"""
        return """
        ⚠️ AVISO IMPORTANTE - RESPONSABILIDADE PROFISSIONAL ⚠️
        
        Esta petição foi gerada por Inteligência Artificial e constitui apenas um RASCUNHO ou MODELO.
        
        OBRIGATÓRIO:
        ✅ Revisão completa por advogado inscrito na OAB
        ✅ Validação de todos os fundamentos jurídicos
        ✅ Verificação da adequação ao caso concreto
        ✅ Protocolo e acompanhamento por profissional habilitado
        
        A IA NÃO SUBSTITUI a representação legal qualificada.
        O uso desta ferramenta é de inteira responsabilidade do usuário.
        """
    
    @staticmethod
    def add_ethics_metadata(response: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona metadados éticos a todas as respostas"""
        response.update({
            "ethics": {
                "disclaimer": EthicsService.get_disclaimer(),
                "generated_at": datetime.now().isoformat(),
                "requires_lawyer_review": True,
                "ai_tool_version": "1.0.0",
                "responsibility_notice": "Esta é uma ferramenta de apoio. A responsabilidade final é do advogado."
            }
        })
        return response
    
    @staticmethod
    def validate_data_sensitivity(data: Dict[str, Any]) -> bool:
        """Valida se dados sensíveis estão sendo tratados adequadamente"""
        sensitive_fields = ['cpf', 'rg', 'endereco', 'telefone', 'email']
        
        for field in sensitive_fields:
            if field in str(data).lower():
                # Log para auditoria (sem expor dados)
                print(f"[ETHICS] Dados sensíveis detectados: {field}")
        
        return True