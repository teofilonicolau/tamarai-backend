# app/modules/trabalhista/service.py - VERSÃO COMPLETA COM ETHICS
from typing import List
from .schemas import DadosTrabalhistas
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class TrabalhistaService:
    
    async def gerar_peticao_vinculo(self, dados: DadosTrabalhistas) -> str:
        """Gera petição de reconhecimento de vínculo empregatício"""
        prompt = f"""
        Como especialista em Direito do Trabalho, baseado nas obras de Mauricio Godinho Delgado 
        e Alice Monteiro de Barros, elabore uma petição inicial para reconhecimento de vínculo 
        empregatício com os seguintes dados:
        
        DADOS DO CASO:
        - Empresa: {dados.empresa_ré}
        - Período: {dados.periodo_trabalho_inicio} a {dados.periodo_trabalho_fim or 'atual'}
        - Cargo: {dados.cargo_funcao}
        - Jornada real: {dados.jornada_real}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS
        3. DO DIREITO (com base na CLT, súmulas TST)
        4. DOS PEDIDOS
        5. DO VALOR DA CAUSA
        
        Use jurisprudência do TST e fundamentos da CLT arts. 2º e 3º.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "trabalhista")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        
        # Adicionar disclaimer ético
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_quesitos_insalubridade(self, dados: DadosTrabalhistas) -> List[str]:
        """Gera quesitos para perícia de insalubridade"""
        return [
            "O ambiente de trabalho do autor apresentava agentes nocivos à saúde?",
            "Quais agentes nocivos foram identificados no local de trabalho?",
            "A exposição aos agentes nocivos estava acima dos limites de tolerância?",
            "Os EPIs fornecidos eram adequados e eficazes?",
            "O uso de EPIs neutralizava completamente a nocividade?",
            "Qual o grau de insalubridade: mínimo (10%), médio (20%) ou máximo (40%)?"
        ]