# app/modules/civil/service.py - CRIAR
from typing import List
from .schemas import DadosCivil
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class CivilService:
    
    async def gerar_peticao_cobranca(self, dados: DadosCivil) -> str:
        """Gera petição de cobrança"""
        prompt = f"""
        Como especialista em Direito Civil, elabore uma petição inicial de cobrança
        com base no Código Civil e os seguintes dados:
        
        DADOS DO CASO:
        - Devedor: {dados.parte_contraria}
        - Valor da dívida: R\$ {dados.valor_divida or dados.valor_causa}
        - Data do fato gerador: {dados.data_fato_gerador}
        - Descrição: {dados.descricao_caso}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS
        3. DO DIREITO (CC arts. 389, 394, 395)
        4. DOS PEDIDOS (principal + juros + correção + custas)
        5. DO VALOR DA CAUSA
        
        Use jurisprudência do STJ sobre cobrança e juros de mora.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "civil")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_peticao_indenizacao(self, dados: DadosCivil) -> str:
        """Gera petição de indenização por danos morais e materiais"""
        prompt = f"""
        Como especialista em Direito Civil, elabore uma petição inicial de indenização
        com base no Código Civil art. 927 e os seguintes dados:
        
        DADOS DO CASO:
        - Causador do dano: {dados.parte_contraria}
        - Danos materiais: R\$ {dados.valor_danos_materiais or 0}
        - Danos morais: R\$ {dados.valor_danos_morais or 0}
        - Data do fato: {dados.data_fato_gerador}
        - Descrição: {dados.descricao_caso}
        
        FUNDAMENTOS:
        - CC art. 927 (responsabilidade civil)
        - CC art. 944 (extensão do dano)
        - Súmula 37 STJ (danos morais cumulativos)
        - Jurisprudência sobre quantum indenizatório
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "civil")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao