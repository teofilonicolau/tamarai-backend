# app/services/ai_service.py - VERSÃO SIMPLIFICADA SEM IMPORTS CIRCULARES
from openai import OpenAI
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Carregar .env diretamente
load_dotenv()

class AIService:
    def __init__(self):
        # Configurar OpenAI diretamente do .env
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
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
        _signature_text = signature_text if signature_text else f"Atenciosamente, Sua IA Jurídica do {_firm_name}"
        _ai_persona = ai_persona if ai_persona else f"Você é um analista jurídico especializado do escritório {_firm_name}."
        
        try:
            prompt = f"""
            {_ai_persona}
            Como especialista jurídico do escritório {_firm_name}, 
            faça um {tipo_analise} do seguinte documento:
            
            {texto}
            
            Inclua:
            - Pontos principais
            - Aspectos jurídicos relevantes
            - Possíveis riscos ou oportunidades
            
            Assine como: {_signature_text}
            """
            
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
            
            prompt = f"""
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

# Instância global
ai_service = AIService()