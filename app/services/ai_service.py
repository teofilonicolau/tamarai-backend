# app/services/ai_service.py - VERSÃO ATUALIZADA COM BRANDING DINÂMICO

from openai import OpenAI
from typing import Dict, Any, Optional
import os

class AIService:
    def __init__(self):
        # Configurar OpenAI diretamente do .env
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    async def fazer_consulta_juridica(
        self, 
        pergunta: str, 
        area: str = "geral",
        firm_name: Optional[str] = None,
        lawyer_name: Optional[str] = None,
        signature_text: Optional[str] = None,
        ai_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fazer consulta jurídica usando OpenAI com branding dinâmico"""
        if not self.client:
            return {
                "resposta": "⚠️ Chave OpenAI não configurada no arquivo .env",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro_configuracao"
            }
        
        # Definir padrões para branding se não forem fornecidos
        _firm_name = firm_name if firm_name else "Serviço Jurídico de IA"
        _lawyer_name = lawyer_name if lawyer_name else "um especialista em Direito"
        _signature_text = signature_text if signature_text else f"Atenciosamente, Sua IA Jurídica do {_firm_name}"
        _ai_persona = ai_persona if ai_persona else f"Você é um assistente jurídico especializado em Direito brasileiro do escritório {_firm_name}."
        
        try:
            # Prompt especializado por área, agora dinâmico
            prompts = {
                "previdenciario": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito Previdenciário brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (Lei 8.213/91, EC 103/2019, Decreto 3.048/99)
                - Jurisprudência relevante (STJ, STF, TNU)
                - Orientações práticas para o cliente
                - Prazos importantes
                - Documentação necessária
                
                Assine como: {_signature_text}
                """,
                "trabalhista": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito do Trabalho brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (CLT, CF/88)
                - Jurisprudência relevante (TST)
                - Direitos do trabalhador
                - Procedimentos práticos
                - Prazos processuais
                
                Assine como: {_signature_text}
                """,
                "consumidor": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito do Consumidor brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (CDC - Lei 8.078/90)
                - Jurisprudência relevante (STJ)
                - Direitos do consumidor
                - Como proceder
                - Órgãos de proteção
                
                Assine como: {_signature_text}
                """,
                "civil": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito Civil brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (Código Civil)
                - Jurisprudência relevante
                - Aspectos práticos
                - Documentação necessária
                - Prazos legais
                
                Assine como: {_signature_text}
                """,
                "processual_civil": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito Processual Civil brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (CPC/2015)
                - Procedimentos corretos
                - Prazos processuais
                - Jurisprudência relevante
                - Recursos cabíveis
                
                Assine como: {_signature_text}
                """,
                "geral": f"""
                {_ai_persona}
                Você é um assistente jurídico geral do escritório {_firm_name}, especializado em Direito brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Forneça uma resposta completa e fundamentada, sempre mencionando que para casos específicos 
                é recomendável consultar {_lawyer_name or 'um profissional do direito'}.
                
                Assine como: {_signature_text}
                """
            }
            
            prompt = prompts.get(area, prompts["geral"])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": _ai_persona},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return {
                "resposta": response.choices[0].message.content,
                "modelo": self.model,
                "tokens_usados": response.usage.total_tokens,
                "area_consultada": area,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "resposta": f"Erro ao processar consulta: {str(e)}",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro"
            }
    
    async def analisar_documento(
        self, 
        texto: str, 
        tipo_analise: str = "resumo",
        firm_name: Optional[str] = None,
        lawyer_name: Optional[str] = None,
        signature_text: Optional[str] = None,
        ai_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analisar documento usando OpenAI com branding dinâmico"""
        if not self.client:
            return {
                "resultado": "⚠️ Chave OpenAI não configurada no arquivo .env",
                "tipo_analise": tipo_analise,
                "palavras": len(texto.split()),
                "caracteres": len(texto),
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro_configuracao"
            }
        
        # Definir padrões para branding se não forem fornecidos
        _firm_name = firm_name if firm_name else "Serviço Jurídico de IA"
        _lawyer_name = lawyer_name if lawyer_name else "um especialista em Direito"
        _signature_text = signature_text if signature_text else f"Atenciosamente, Sua IA Jurídica do {_firm_name}"
        _ai_persona = ai_persona if ai_persona else f"Você é um analista jurídico especializado do escritório {_firm_name}."
        
        try:
            prompts_analise = {
                "resumo": f"""
                {_ai_persona}
                Como especialista jurídico do escritório {_firm_name}, 
                faça um resumo executivo do seguinte documento:
                
                {texto}
                
                Inclua:
                - Pontos principais
                - Aspectos jurídicos relevantes
                - Possíveis riscos ou oportunidades
                
                Assine como: {_signature_text}
                """,
                "pontos_chave": f"""
                {_ai_persona}
                Como especialista jurídico, identifique os pontos-chave 
                do seguinte documento:
                
                {texto}
                
                Organize por:
                - Aspectos legais
                - Cláusulas importantes
                - Direitos e obrigações
                
                Assine como: {_signature_text}
                """,
                "riscos": f"""
                {_ai_persona}
                Como especialista jurídico, analise os riscos jurídicos 
                do seguinte documento:
                
                {texto}
                
                Identifique:
                - Riscos contratuais
                - Riscos processuais
                - Recomendações preventivas
                
                Assine como: {_signature_text}
                """,
                "sugestoes": f"""
                {_ai_persona}
                Como especialista jurídico, forneça sugestões de melhoria 
                para o seguinte documento:
                
                {texto}
                
                Sugira:
                - Melhorias na redação
                - Cláusulas adicionais
                - Proteções jurídicas
                
                Assine como: {_signature_text}
                """
            }
            
            prompt = prompts_analise.get(tipo_analise, prompts_analise["resumo"])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": _ai_persona},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            return {
                "resultado": response.choices[0].message.content,
                "tipo_analise": tipo_analise,
                "palavras": len(texto.split()),
                "caracteres": len(texto),
                "modelo": self.model,
                "tokens_usados": response.usage.total_tokens,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "resultado": f"Erro ao analisar documento: {str(e)}",
                "tipo_analise": tipo_analise,
                "palavras": len(texto.split()),
                "caracteres": len(texto),
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro"
            }

    async def gerar_relatorio_juridico(
        self, 
        titulo: str, 
        conteudo: str, 
        area: str = "geral", 
        incluir_jurisprudencia: bool = True,
        firm_name: Optional[str] = None,
        lawyer_name: Optional[str] = None,
        signature_text: Optional[str] = None,
        ai_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gerar relatório jurídico estruturado com branding dinâmico"""
        if not self.client:
            return {
                "relatorio": "⚠️ Chave OpenAI não configurada no arquivo .env",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro_configuracao"
            }
        
        # Definir padrões para branding se não forem fornecidos
        _firm_name = firm_name if firm_name else "Serviço Jurídico de IA"
        _lawyer_name = lawyer_name if lawyer_name else "um especialista em Direito"
        _signature_text = signature_text if signature_text else f"Atenciosamente, Sua IA Jurídica do {_firm_name}"
        _ai_persona = ai_persona if ai_persona else f"Você é um especialista em elaboração de pareceres jurídicos do escritório {_firm_name}."
        
        try:
            # Prompt para geração de relatório
            jurisprudencia_instrucao = "Inclua jurisprudência relevante e precedentes." if incluir_jurisprudencia else "Não inclua jurisprudência."
            
            prompts_relatorio = {
                "previdenciario": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito Previdenciário brasileiro.
                Gere um parecer jurídico estruturado sobre o seguinte tema:
                
                TÍTULO: {titulo}
                CONTEÚDO: {conteudo}
                
                Estruture o parecer com:
                1. INTRODUÇÃO
                2. FUNDAMENTAÇÃO LEGAL (Lei 8.213/91, EC 103/2019, Decreto 3.048/99)
                3. ANÁLISE TÉCNICA PREVIDENCIÁRIA
                4. JURISPRUDÊNCIA RELEVANTE (STJ, STF, TNU) - {jurisprudencia_instrucao}
                5. CONCLUSÃO E RECOMENDAÇÕES
                
                Assine como: {_signature_text}
                """,
                "trabalhista": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito do Trabalho brasileiro.
                Gere um parecer jurídico estruturado sobre o seguinte tema:
                
                TÍTULO: {titulo}
                CONTEÚDO: {conteudo}
                
                Estruture o parecer com:
                1. INTRODUÇÃO
                2. FUNDAMENTAÇÃO LEGAL (CLT, CF/88)
                3. ANÁLISE DOS DIREITOS TRABALHISTAS
                4. JURISPRUDÊNCIA DO TST - {jurisprudencia_instrucao}
                5. CONCLUSÃO E ORIENTAÇÕES PRÁTICAS
                
                Assine como: {_signature_text}
                """,
                "consumidor": f"""
                {_ai_persona}
                Você atua como {_lawyer_name}, especialista em Direito do Consumidor brasileiro.
                Gere um parecer jurídico estruturado sobre o seguinte tema:
                
                TÍTULO: {titulo}
                CONTEÚDO: {conteudo}
                
                Estruture o parecer com:
                1. INTRODUÇÃO
                2. FUNDAMENTAÇÃO LEGAL (CDC - Lei 8.078/90)
                3. ANÁLISE DOS DIREITOS DO CONSUMIDOR
                4. JURISPRUDÊNCIA DO STJ - {jurisprudencia_instrucao}
                5. CONCLUSÃO E MEDIDAS RECOMENDADAS
                
                Assine como: {_signature_text}
                """,
                "geral": f"""
                {_ai_persona}
                Você é um assistente jurídico do escritório {_firm_name}.
                Gere um parecer jurídico estruturado sobre o seguinte tema:
                
                TÍTULO: {titulo}
                CONTEÚDO: {conteudo}
                
                Estruture o parecer com:
                1. INTRODUÇÃO
                2. FUNDAMENTAÇÃO LEGAL
                3. ANÁLISE JURÍDICA
                4. PRECEDENTES - {jurisprudencia_instrucao}
                5. CONCLUSÃO E RECOMENDAÇÕES
                
                Assine como: {_signature_text}
                """
            }
            
            prompt = prompts_relatorio.get(area, prompts_relatorio["geral"])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": _ai_persona},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2
            )
            
            return {
                "relatorio": response.choices[0].message.content,
                "modelo": self.model,
                "tokens_usados": response.usage.total_tokens,
                "incluiu_jurisprudencia": incluir_jurisprudencia,
                "area": area,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "relatorio": f"Erro ao gerar parecer: {str(e)}",
                "modelo": self.model,
                "tokens_usados": 0,
                "incluiu_jurisprudencia": incluir_jurisprudencia,
                "status": "erro"
            }

    async def gerar_peticao(
        self, 
        dados_peticao: Dict[str, Any], 
        area_juridica: str,
        firm_name: Optional[str] = None,
        lawyer_name: Optional[str] = None,
        signature_text: Optional[str] = None,
        ai_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gerar petição jurídica com IA e branding dinâmico"""
        if not self.client:
            return {
                "texto_peticao": "⚠️ Chave OpenAI não configurada no arquivo .env",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro_configuracao"
            }
        
        # Definir padrões para branding se não forem fornecidos
        _firm_name = firm_name if firm_name else "Serviço Jurídico de IA"
        _lawyer_name = lawyer_name if lawyer_name else "um especialista em Direito"
        _signature_text = signature_text if signature_text else f"Atenciosamente, {_lawyer_name} - {_firm_name}"
        _ai_persona = ai_persona if ai_persona else f"Você é {_lawyer_name}, advogado especialista em redação de petições jurídicas brasileiras do escritório {_firm_name}."
        
        try:
            # Construir prompt especializado para petições
            prompt = self._construir_prompt_peticao(dados_peticao, area_juridica, _firm_name, _lawyer_name, _signature_text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": _ai_persona},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.2
            )
            
            return {
                "texto_peticao": response.choices[0].message.content,
                "modelo": self.model,
                "tokens_usados": response.usage.total_tokens,
                "jurisprudencia_utilizada": [],  # Implementar busca real
                "legislacao_aplicada": [],       # Implementar busca real
                "prompt_utilizado": prompt,
                "area_juridica": area_juridica,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "texto_peticao": f"Erro ao gerar petição: {str(e)}",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro"
            }

    def _construir_prompt_peticao(
        self, 
        dados: Dict[str, Any], 
        area: str, 
        firm_name: str, 
        lawyer_name: str, 
        signature_text: str
    ) -> str:
        """Construir prompt especializado para geração de petições com branding dinâmico"""
        
        dados_autor = dados.get('dados_autor', {})
        dados_especificos = dados.get('dados_especificos', {})
        pedidos = dados.get('pedidos', {})
        
        prompt = f"""
        Você é {lawyer_name}, advogado especialista em {area.replace('_', ' ').title()} do escritório {firm_name}.
        
        Gere uma petição inicial completa e profissional com base nos dados fornecidos:
        
        DADOS DO AUTOR:
        - Nome: {dados_autor.get('nome', '')}
        - CPF: {dados_autor.get('cpf', '')}
        - RG: {dados_autor.get('rg', '')} - {dados_autor.get('orgao_emissor', '')}
        - Nacionalidade: {dados_autor.get('nacionalidade', 'brasileira')}
        - Estado Civil: {dados_autor.get('estado_civil', '')}
        - Profissão: {dados_autor.get('profissao', '')}
        - Endereço: {dados_autor.get('endereco_completo', '')}
        - Email: {dados_autor.get('email', '')}
        - Telefone: {dados_autor.get('telefone', '')}
        
        DADOS ESPECÍFICOS:
        {self._formatar_dados_especificos(dados_especificos, area)}
        
        PEDIDOS:
        - Pedido Principal: {pedidos.get('pedido_principal', '')}
        - Valor da Causa: R\$ {pedidos.get('valor_causa', 0):,.2f}
        - Gratuidade de Justiça: {'Sim' if pedidos.get('gratuidade_justica') else 'Não'}
        - Tutela de Urgência: {'Sim' if pedidos.get('tutela_urgencia') else 'Não'}
        - Audiência de Conciliação: {'Sim' if pedidos.get('audiencia_conciliacao') else 'Não'}
        
        ESTRUTURA OBRIGATÓRIA:
        1. EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DE DIREITO DA ___ª VARA CÍVEL
        2. QUALIFICAÇÃO DAS PARTES
        3. DOS FATOS
        4. DO DIREITO (fundamentação legal específica da área)
        5. DOS PEDIDOS
        6. REQUERIMENTOS FINAIS
        7. ASSINATURA DO ADVOGADO
        
        INSTRUÇÕES ESPECÍFICAS:
        - Use linguagem jurídica formal e técnica
        - Cite a legislação pertinente à área de {area.replace('_', ' ')}
        - Formate adequadamente com numeração e parágrafos
        - Seja preciso e objetivo
        - Inclua todos os elementos processuais necessários
        - Termine com a assinatura: "{signature_text}"
        
        Gere a petição completa:
        """
        
        return prompt

    def _formatar_dados_especificos(self, dados: Dict[str, Any], area: str) -> str:
        """Formatar dados específicos por área jurídica"""
        if area == "previdenciario":
            return f"""
            - Tipo de Benefício: {dados.get('tipo_beneficio', '')}
            - DER (Data de Entrada do Requerimento): {dados.get('der', '')}
            - Número do Processo Administrativo: {dados.get('numero_processo_administrativo', 'Não informado')}
            - Motivo da Recusa: {dados.get('motivo_recusa', '')}
            - Histórico Laboral: {dados.get('historico_laboral', 'A ser detalhado')}
            - Informações Médicas: {dados.get('informacoes_medicas', 'Conforme laudos anexos')}
            """
        elif area == "consumidor":
            return f"""
            - Tipo de Problema: {dados.get('tipo_problema', '')}
            - Empresa Ré: {dados.get('empresa_ré', '')}
            - CNPJ da Empresa: {dados.get('cnpj_empresa', '')}
            - Endereço da Empresa: {dados.get('endereco_empresa', '')}
            - Descrição do Problema: {dados.get('descricao_problema', '')}
            - Valor do Prejuízo: R\$ {dados.get('valor_prejuizo', 0):,.2f}
            - Data da Ocorrência: {dados.get('data_ocorrencia', '')}
            """
        elif area == "trabalhista":
            return f"""
            - Empresa: {dados.get('empresa', '')}
            - Período de Trabalho: {dados.get('periodo_trabalho', '')}
            - Função: {dados.get('funcao', '')}
            - Salário: R\$ {dados.get('salario', 0):,.2f}
            - Tipo de Rescisão: {dados.get('tipo_rescisao', '')}
            - Direitos Pleiteados: {dados.get('direitos_pleiteados', '')}
            """
        else:
            return str(dados)

# Instância global
ai_service = AIService()