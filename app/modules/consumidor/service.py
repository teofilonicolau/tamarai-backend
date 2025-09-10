# app/modules/consumidor/service.py - CORRIGIDO
from typing import List
from .schemas import DadosConsumidor
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class ConsumidorService:
    
    async def gerar_peticao_vicio_produto(self, dados: DadosConsumidor) -> str:
        """Gera petição para vício do produto"""
        valor_formatado = f"R\$ {dados.valor_prejuizo or 0}"
        
        prompt = f"""
        Como especialista em Direito do Consumidor, elabore uma petição inicial para vício do produto
        com base no CDC (Lei 8.078/90) e os seguintes dados:
        
        DADOS DO CASO:
        - Empresa: {dados.empresa_ré}
        - Problema: {dados.descricao_problema}
        - Data: {dados.data_ocorrencia}
        - Valor: {valor_formatado}
        
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
        disclaimer = EthicsService.get_disclaimer()
        peticao += f"\n\n{disclaimer}"
        
        return peticao
    
    async def gerar_peticao_cobranca_indevida(self, dados: DadosConsumidor) -> str:
        """Gera petição para cobrança indevida"""
        
        # Verificar se houve pagamento efetivo
        pagamento_efetuado = "pago" in dados.descricao_problema.lower() or dados.valor_prejuizo > 0
        valor_formatado = f"R\$ {dados.valor_prejuizo or 0}"
        
        # Criar texto condicional fora da f-string
        texto_pagamento = ""
        if pagamento_efetuado:
            texto_pagamento = f"Se houve pagamento, mencionar: 'Tendo o Autor efetuado o pagamento das cobranças indevidas no valor de {valor_formatado}...'"
        else:
            texto_pagamento = "Se não houve pagamento, focar na cobrança vexatória e danos morais."
        
        prompt = f"""
        Como especialista em Direito do Consumidor, elabore uma petição inicial para cobrança indevida
        com base no CDC art. 42 parágrafo único e os seguintes dados:
        
        DADOS DO CASO:
        - Empresa: {dados.empresa_ré}
        - Descrição: {dados.descricao_problema}
        - Valor cobrado indevidamente: {valor_formatado}
        - Pagamento efetuado: {"Sim" if pagamento_efetuado else "Apenas cobrança"}
        
        FUNDAMENTOS:
        - CDC art. 42 parágrafo único (devolução em dobro)
        - Danos morais por cobrança vexatória
        - Jurisprudência STJ sobre repetição de indébito
        
        IMPORTANTE: 
        {texto_pagamento}
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "consumidor")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        disclaimer = EthicsService.get_disclaimer()
        peticao += f"\n\n{disclaimer}"
        
        return peticao