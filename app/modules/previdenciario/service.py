# app/modules/previdenciario/service.py - NOVO
from typing import List
from .schemas import DadosPrevidenciarios
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class PrevidenciarioService:
    
    async def gerar_peticao_aposentadoria_invalidez(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para aposentadoria por invalidez"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para aposentadoria
        por invalidez com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Tipo: {dados.tipo_beneficio}
        - DER: {dados.der}
        - Motivo da recusa: {dados.motivo_recusa}
        - CID: {dados.cid_principal or 'A definir'}
        
        HISTÓRICO DETALHADO:
        - Histórico laboral: {dados.historico_laboral or 'A informar'}
        - Atividade especial: {"Sim" if dados.atividade_especial else "Não"}
        - Exposição a agentes nocivos: {dados.exposicao_agentes_nocivos or 'Não informado'}
        - Informações médicas: {dados.informacoes_medicas or 'A detalhar'}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (incluir histórico laboral detalhado e exposição ocupacional)
        3. DO DIREITO (Lei 8.213/91 art. 42)
        4. DOS PEDIDOS
        5. DO VALOR DA CAUSA
        
        DOCUMENTOS ESPECÍFICOS:
        {', '.join(dados.laudos_medicos) if dados.laudos_medicos else 'Laudos médicos a anexar'}
        
        Use jurisprudência da TNU e STJ sobre incapacidade laboral.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_peticao_revisao_vida_toda(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para Revisão da Vida Toda"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para Revisão da Vida Toda
        com base na decisão do STF (RE 1.276.977) e os seguintes dados:
        
        DADOS DO CASO:
        - Benefício: {dados.numero_beneficio or 'A informar'}
        - DIB: {dados.dib or 'A informar'}
        - Tempo de contribuição: {dados.tempo_contribuicao_total or 0} meses
        - Histórico contributivo: {dados.historico_contribuicoes or 'A detalhar'}
        
        FUNDAMENTOS ESPECÍFICOS:
        - STF RE 1.276.977 (repercussão geral)
        - Inclusão de salários anteriores a julho/1994
        - Cálculo mais benéfico ao segurado
        - Prescrição quinquenal das parcelas
        
        VALIDAÇÃO OBRIGATÓRIA:
        Incluir: "Conforme simulação técnica anexa, a inclusão das contribuições anteriores a julho/1994 
        resulta em um aumento significativo do benefício, comprovando ser a opção mais vantajosa ao segurado, 
        considerando os salários relevantes do período pré-Plano Real."
        
        HISTÓRICO CONTRIBUTIVO:
        Detalhar que o segurado possui contribuições desde {dados.historico_laboral or '1988'} com salários 
        expressivos antes de 1994.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao