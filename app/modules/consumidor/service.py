# app/modules/consumidor/service.py - NOVO
from typing import List
from .schemas import DadosConsumidor
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class ConsumidorService:
    
    async def gerar_peticao_vicio_produto(self, dados: DadosConsumidor) -> str:
        """Gera petição para vício do produto"""
        prompt = f"""
        Como especialista em Direito do Consumidor, elabore uma petição inicial para vício do produto
        com base no CDC (Lei 8.078/90) e os seguintes dados:
        
        DADOS DO CASO:
        - Empresa: {dados.empresa_ré}
        - Problema: {dados.descricao_problema}
        - Data: {dados.data_ocorrencia}
        - Valor: R\$ {dados.valor_prejuizo or 0}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS
        3. DO DIREITO (CDC arts. 18, 19, 20)
        4. DOS PEDIDOS
        5. DO VALOR DA CAUSA
        
        Use jurisprudência do STJ sobre responsabilidade objetiva.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "consumidor")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        
        # Adicionar disclaimer ético
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_peticao_cobranca_indevida(self, dados: DadosConsumidor) -> str:
        """Gera petição para cobrança indevida"""
        
        # Verificar se houve pagamento efetivo
        pagamento_efetuado = "pago" in dados.descricao_problema.lower() or dados.valor_prejuizo > 0
        
        prompt = f"""
        Como especialista em Direito do Consumidor, elabore uma petição inicial para cobrança indevida
        com base no CDC art. 42 parágrafo único e os seguintes dados:
        
        DADOS DO CASO:
        - Empresa: {dados.empresa_ré}
        - Descrição: {dados.descricao_problema}
        - Valor cobrado indevidamente: R\$ {dados.valor_prejuizo or 0}
        - Pagamento efetuado: {"Sim" if pagamento_efetuado else "Apenas cobrança"}
        
        FUNDAMENTOS:
        - CDC art. 42 parágrafo único (devolução em dobro)
        - Danos morais por cobrança vexatória
        - Jurisprudência STJ sobre repetição de indébito
        
        IMPORTANTE: 
        {"Se houve pagamento, mencionar: 'Tendo o Autor efetuado o pagamento das cobranças indevidas no valor de R\$ " + str(dados.valor_prejuizo or 0) + "...'" if pagamento_efetuado else "Se não houve pagamento, focar na cobrança vexatória e danos morais."}
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "consumidor")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao