# app/modules/processual_civil/service.py - CRIAR
from typing import List
from .schemas import DadosProcessualCivil
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class ProcessualCivilService:
    
    async def gerar_peticao_execucao(self, dados: DadosProcessualCivil) -> str:
        """Gera petição de execução de título extrajudicial"""
        
        # Calcular detalhamento da dívida
        valor_mensal = dados.valor_aluguel or (dados.valor_execucao / (dados.meses_atraso or 1))
        meses = dados.meses_atraso or 1
        
        prompt = f"""
        Como especialista em Direito Processual Civil, elabore uma petição inicial de execução
        com base no CPC/2015 e os seguintes dados:
        
        DADOS DO CASO:
        - Executado: {dados.parte_contraria}
        - Valor da execução: R\$ {dados.valor_execucao or 0}
        - Título executivo: {dados.titulo_executivo or 'A especificar'}
        - Data vencimento: {dados.data_vencimento or 'A informar'}
        
        DETALHAMENTO DA DÍVIDA:
        - Valor mensal: R\$ {valor_mensal:.2f}
        - Meses em atraso: {meses}
        - Valor principal: R\$ {valor_mensal * meses:.2f}
        - Juros e multas: [Calcular conforme contrato]
        - Total atualizado: R\$ {dados.valor_execucao or 0}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DO TÍTULO EXECUTIVO
        3. DO CÁLCULO DETALHADO (especificar cada parcela em atraso)
        4. DOS PEDIDOS (penhora, avaliação, alienação)
        5. DO VALOR DA CAUSA
        
        TRANSPARÊNCIA: Incluir planilha detalhada mostrando cada mês em atraso,
        valor individual e cálculo de juros/multas.
        
        Base legal: CPC arts. 771 a 925 (execução).
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "processual_civil")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_peticao_monitoria(self, dados: DadosProcessualCivil) -> str:
        """Gera petição de ação monitória"""
        prompt = f"""
        Como especialista em Direito Processual Civil, elabore uma petição inicial de ação monitória
        com base no CPC/2015 arts. 700-702 e os seguintes dados:
        
        DADOS DO CASO:
        - Requerido: {dados.parte_contraria}
        - Valor: R\$ {dados.valor_execucao or 0}
        - Descrição: {dados.descricao_pedido}
        
        FUNDAMENTOS:
        - CPC art. 700 (prova escrita sem eficácia de título executivo)
        - Procedimento monitório
        - Mandado de pagamento ou entrega
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "processual_civil")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao