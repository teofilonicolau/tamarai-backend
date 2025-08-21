# app/services/ai_service.py (VERSÃO SIMPLIFICADA)
from openai import OpenAI
from typing import Dict, Any
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
    
    async def fazer_consulta_juridica(self, pergunta: str, area: str = "geral") -> Dict[str, Any]:
        """Fazer consulta jurídica usando OpenAI"""
        if not self.client:
            return {
                "resposta": "⚠️ Chave OpenAI não configurada no arquivo .env",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro_configuracao"
            }
        
        try:
            # Prompt especializado por área
            prompts = {
                "previdenciario": f"""
                Você é um especialista em Direito Previdenciário brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal
                - Jurisprudência relevante
                - Orientações práticas
                """,
                "consumidor": f"""
                Você é um especialista em Direito do Consumidor brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Inclua:
                - Base legal (CDC)
                - Jurisprudência relevante
                - Direitos do consumidor
                """,
                "geral": f"""
                Você é um assistente jurídico especializado em Direito brasileiro.
                Responda de forma técnica e precisa à seguinte pergunta:
                
                {pergunta}
                
                Forneça uma resposta completa e fundamentada.
                """
            }
            
            prompt = prompts.get(area, prompts["geral"])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico especializado em Direito brasileiro."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return {
                "resposta": response.choices[0].message.content,
                "modelo": self.model,
                "tokens_usados": response.usage.total_tokens,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "resposta": f"Erro ao processar consulta: {str(e)}",
                "modelo": self.model,
                "tokens_usados": 0,
                "status": "erro"
            }
    
    async def analisar_documento(self, texto: str, tipo_analise: str = "resumo") -> Dict[str, Any]:
        """Analisar documento usando OpenAI"""
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
        
        try:
            prompts_analise = {
                "resumo": f"Faça um resumo executivo do seguinte texto:\n\n{texto}",
                "pontos_chave": f"Identifique os pontos-chave do seguinte documento:\n\n{texto}",
                "riscos": f"Analise os riscos jurídicos do seguinte documento:\n\n{texto}",
                "sugestoes": f"Forneça sugestões de melhoria para o seguinte documento:\n\n{texto}"
            }
            
            prompt = prompts_analise.get(tipo_analise, prompts_analise["resumo"])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um analista jurídico especializado."},
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

# Instância global
ai_service = AIService()