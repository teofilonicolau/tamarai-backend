# app/services/ai_service.py
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
import json
import hashlib
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.rag_service import RAGService

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache = CacheService()
        self.rag = RAGService()
        
    async def consulta_juridica_especializada(
        self, 
        pergunta: str, 
        area_juridica: str,
        incluir_jurisprudencia: bool = True,
        incluir_legislacao: bool = True
    ) -> Dict[str, Any]:
        """Consulta jurídica especializada com RAG"""
        
        # Verificar cache primeiro
        cache_key = self._generate_cache_key(pergunta, area_juridica)
        cached_response = await self.cache.get_ai_response(cache_key)
        if cached_response:
            return json.loads(cached_response)
        
        # Buscar contexto jurídico relevante
        contexto = await self._buscar_contexto_juridico(
            pergunta, area_juridica, incluir_jurisprudencia, incluir_legislacao
        )
        
        # Construir prompt especializado
        prompt = self._construir_prompt_especializado(pergunta, area_juridica, contexto)
        
        # Gerar resposta com IA
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt(area_juridica)
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        resposta_texto = response.choices[0].message.content
        
        # Estruturar resposta
        resultado = {
            "resposta": resposta_texto,
            "area_juridica": area_juridica,
            "jurisprudencia_utilizada": contexto.get("jurisprudencia", []),
            "legislacao_aplicada": contexto.get("legislacao", []),
            "palavras_chave": self._extrair_palavras_chave(pergunta),
            "tempo_resposta": response.usage.total_tokens if response.usage else 0
        }
        
        # Salvar no cache
        await self.cache.set_ai_response(cache_key, json.dumps(resultado))
        
        return resultado
    
    async def gerar_peticao(
        self, 
        dados_peticao: Dict[str, Any], 
        area_juridica: str
    ) -> Dict[str, Any]:
        """Gera petição completa com IA"""
        
        # Buscar contexto jurídico específico para o caso
        contexto = await self._buscar_contexto_para_peticao(dados_peticao, area_juridica)
        
        # Construir prompt para geração de petição
        prompt = self._construir_prompt_peticao(dados_peticao, area_juridica, contexto)
        
        # Gerar petição com IA
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt_peticao(area_juridica)
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,  # Mais determinístico para petições
            max_tokens=4000
        )
        
        texto_peticao = response.choices[0].message.content
        
        return {
            "texto_peticao": texto_peticao,
            "jurisprudencia_utilizada": contexto.get("jurisprudencia", []),
            "legislacao_aplicada": contexto.get("legislacao", []),
            "prompt_utilizado": prompt[:500] + "..." if len(prompt) > 500 else prompt
        }
    
    def _get_system_prompt(self, area_juridica: str) -> str:
        """Prompts especializados por área jurídica"""
        
        prompts = {
            "previdenciario": """
            Você é um advogado especialista em Direito Previdenciário brasileiro, com profundo conhecimento em:
            - Lei 8.213/91 (Lei de Benefícios da Previdência Social)
            - Decreto 3.048/99 (Regulamento da Previdência Social)
            - Instrução Normativa 128/2022 do INSS
            - Jurisprudência da TNU, STJ e STF
            - Doutrina dos principais autores (Martinez, Sabbag, etc.)
            
            Responda sempre com:
            1. Fundamentação legal precisa
            2. Citação de jurisprudência relevante
            3. Linguagem técnica jurídica
            4. Orientações práticas
            5. Análise crítica quando necessário
            """,
            
            "consumidor": """
            Você é um advogado especialista em Direito do Consumidor brasileiro, com expertise em:
            - Código de Defesa do Consumidor (Lei 8.078/90)
            - Jurisprudência do STJ sobre relações de consumo
            - Doutrina especializada (Tartuce, Cavalieri Filho, etc.)
            - Práticas abusivas e vícios de produtos/serviços
            - Responsabilidade civil do fornecedor
            
            Responda sempre com:
            1. Aplicação precisa do CDC
            2. Jurisprudência consolidada
            3. Análise de responsabilidade
            4. Cálculo de danos quando aplicável
            5. Estratégias processuais
            """,
            
            "processual_civil": """
            Você é um advogado especialista em Direito Processual Civil brasileiro, com domínio em:
            - Código de Processo Civil (Lei 13.105/15)
            - Jurisprudência dos tribunais superiores
            - Doutrina processualista (Didier Jr., Dinamarco, etc.)
            - Técnicas de peticionamento
            - Recursos e procedimentos especiais
            
            Responda sempre com:
            1. Fundamentação processual correta
            2. Prazos e procedimentos
            3. Jurisprudência aplicável
            4. Técnica processual adequada
            5. Estratégia processual
            """
        }
        
        return prompts.get(area_juridica, prompts["previdenciario"])
    
    def _get_system_prompt_peticao(self, area_juridica: str) -> str:
        """Prompts específicos para geração de petições"""
        
        base_prompt = """
        Você é um advogado experiente especializado em redigir petições jurídicas de alta qualidade.
        
        INSTRUÇÕES PARA REDAÇÃO:
        1. Use linguagem jurídica formal e técnica
        2. Estruture a petição conforme padrões forenses
        3. Aplique as regras de tipografia jurídica de Thomé Sabbag
        4. Cite jurisprudência e legislação de forma precisa
        5. Mantenha coerência argumentativa
        6. Use formatação adequada (negrito para títulos, etc.)
        
        ESTRUTURA OBRIGATÓRIA:
        1. EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A)...
        2. Qualificação das partes
        3. DOS FATOS
        4. DO DIREITO
        5. DOS PEDIDOS
        6. Valor da causa
        7. Requerimentos finais
        8. Local, data e assinatura
        """
        
        area_specific = {
            "previdenciario": """
            ESPECIALIZAÇÃO PREVIDENCIÁRIA:
            - Cite sempre a Lei 8.213/91 e Decreto 3.048/99
            - Use jurisprudência da TNU e STJ
            - Mencione a DER (Data de Entrada do Requerimento)
            - Fundamente o direito adquirido quando aplicável
            - Solicite tutela de urgência quando cabível
            """,
            
            "consumidor": """
            ESPECIALIZAÇÃO CONSUMIDOR:
            - Aplique o CDC (Lei 8.078/90) de forma precisa
            - Cite jurisprudência do STJ sobre consumo
            - Fundamente responsabilidade objetiva
            - Calcule danos materiais e morais
            - Solicite inversão do ônus da prova
            """,
            
            "processual_civil": """
            ESPECIALIZAÇÃO PROCESSUAL:
            - Aplique o CPC (Lei 13.105/15) corretamente
            - Observe competência e procedimento
            - Fundamente pedidos de forma técnica
            - Cite jurisprudência processual
            - Respeite prazos e formalidades
            """
        }
        
        return base_prompt + "\n\n" + area_specific.get(area_juridica, "")
    
    async def _buscar_contexto_juridico(
        self, 
        pergunta: str, 
        area_juridica: str,
        incluir_jurisprudencia: bool,
        incluir_legislacao: bool
    ) -> Dict[str, Any]:
        """Busca contexto jurídico relevante usando RAG"""
        
        contexto = {}
        
        if incluir_jurisprudencia:
            jurisprudencia = await self.rag.buscar_jurisprudencia(
                area_juridica, 
                self._extrair_palavras_chave(pergunta)
            )
            contexto["jurisprudencia"] = jurisprudencia
        
        if incluir_legislacao:
            legislacao = await self.rag.buscar_legislacao(area_juridica, pergunta)
            contexto["legislacao"] = legislacao
        
        return contexto
    
    async def _buscar_contexto_para_peticao(
        self, 
        dados_peticao: Dict[str, Any], 
        area_juridica: str
    ) -> Dict[str, Any]:
        """Busca contexto específico para geração de petição"""
        
        # Extrair palavras-chave dos dados da petição
        palavras_chave = []
        
        if area_juridica == "previdenciario":
            palavras_chave.extend([
                dados_peticao.get("dados_especificos", {}).get("tipo_beneficio", ""),
                dados_peticao.get("dados_especificos", {}).get("motivo_recusa", "")
            ])
        elif area_juridica == "consumidor":
            palavras_chave.extend([
                dados_peticao.get("dados_especificos", {}).get("tipo_problema", ""),
                dados_peticao.get("dados_especificos", {}).get("empresa_ré", "")
            ])
        
        # Filtrar palavras vazias
        palavras_chave = [p for p in palavras_chave if p and len(p) > 2]
        
        # Buscar contexto
        contexto = {}
        
        jurisprudencia = await self.rag.buscar_jurisprudencia(area_juridica, palavras_chave)
        contexto["jurisprudencia"] = jurisprudencia
        
        legislacao = await self.rag.buscar_legislacao(area_juridica, " ".join(palavras_chave))
        contexto["legislacao"] = legislacao
        
        return contexto
    
    def _construir_prompt_especializado(
        self, 
        pergunta: str, 
        area_juridica: str, 
        contexto: Dict[str, Any]
    ) -> str:
        """Constrói prompt especializado com contexto jurídico"""
        
        prompt = f"""
        CONSULTA JURÍDICA - ÁREA: {area_juridica.upper()}
        
        PERGUNTA DO CLIENTE:
        {pergunta}
        
        CONTEXTO JURÍDICO RELEVANTE:
        """
        
        if contexto.get("jurisprudencia"):
            prompt += "\n\nJURISPRUDÊNCIA APLICÁVEL:\n"
            for i, jurisp in enumerate(contexto["jurisprudencia"][:3], 1):
                prompt += f"{i}. {jurisp.get('ementa', '')[:200]}...\n"
        
        if contexto.get("legislacao"):
            prompt += "\n\nLEGISLAÇÃO APLICÁVEL:\n"
            for i, lei in enumerate(contexto["legislacao"][:3], 1):
                prompt += f"{i}. {lei.get('artigo', '')} - {lei.get('texto', '')[:200]}...\n"
        
        prompt += """
        
        INSTRUÇÃO:
        Com base na pergunta e no contexto jurídico fornecido, elabore uma resposta completa e especializada que:
        1. Responda diretamente à pergunta
        2. Cite a legislação aplicável
        3. Mencione jurisprudência relevante
        4. Forneça orientações práticas
        5. Use linguagem técnica jurídica apropriada
        """
        
        return prompt
    
    def _construir_prompt_peticao(
        self, 
        dados_peticao: Dict[str, Any], 
        area_juridica: str, 
        contexto: Dict[str, Any]
    ) -> str:
        """Constrói prompt para geração de petição"""
        
        prompt = f"""
        GERAÇÃO DE PETIÇÃO - ÁREA: {area_juridica.upper()}
        
        DADOS DO CASO:
        
        AUTOR:
        Nome: {dados_peticao['dados_autor']['nome']}
        CPF: {dados_peticao['dados_autor']['cpf']}
        RG: {dados_peticao['dados_autor']['rg']}
        Endereço: {dados_peticao['dados_autor']['endereco_completo']}
        
        DADOS ESPECÍFICOS:
        """
        
        # Adicionar dados específicos por área
        for key, value in dados_peticao.get("dados_especificos", {}).items():
            prompt += f"{key}: {value}\n"
        
        prompt += f"""
        
        PEDIDOS:
        Principal: {dados_peticao['pedidos']['pedido_principal']}
        Retroativo: {'Sim' if dados_peticao['pedidos']['pedido_retroativo'] else 'Não'}
        Gratuidade de Justiça: {'Sim' if dados_peticao['pedidos']['gratuidade_justica'] else 'Não'}
        Tutela de Urgência: {'Sim' if dados_peticao['pedidos']['tutela_urgencia'] else 'Não'}
        Valor da Causa: R\$ {dados_peticao['pedidos']['valor_causa']:,.2f}
        """
        
        # Adicionar contexto jurídico
        if contexto.get("jurisprudencia"):
            prompt += "\n\nJURISPRUDÊNCIA PARA FUNDAMENTAÇÃO:\n"
            for jurisp in contexto["jurisprudencia"][:2]:
                prompt += f"- {jurisp.get('ementa', '')[:300]}...\n"
        
        if contexto.get("legislacao"):
            prompt += "\n\nLEGISLAÇÃO APLICÁVEL:\n"
            for lei in contexto["legislacao"][:3]:
                prompt += f"- {lei.get('artigo', '')} - {lei.get('texto', '')[:200]}...\n"
        
        prompt += """
        
        INSTRUÇÃO:
        Redige uma petição inicial completa e profissional com base nos dados fornecidos.
        A petição deve seguir rigorosamente os padrões forenses brasileiros e incluir:
        
        1. Cabeçalho formal dirigido ao juízo
        2. Qualificação completa das partes
        3. Seção "DOS FATOS" narrando o caso
        4. Seção "DO DIREITO" com fundamentação jurídica
        5. Seção "DOS PEDIDOS" com todos os requerimentos
        6. Valor da causa
        7. Requerimentos finais (provas, citação, etc.)
        8. Fecho respeitoso
        
        Use formatação adequada com **negrito** para títulos e seções importantes.
        """
        
        return prompt
    
    def _extrair_palavras_chave(self, texto: str) -> List[str]:
        """Extrai palavras-chave relevantes do texto"""
        # Implementação simples - pode ser melhorada com NLP
        palavras_irrelevantes = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'da', 'do', 'das', 'dos',
            'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'sobre', 'entre',
            'e', 'ou', 'mas', 'que', 'se', 'quando', 'onde', 'como', 'porque', 'então'
        }
        
        palavras = texto.lower().split()
        palavras_chave = [
            palavra for palavra in palavras 
            if len(palavra) > 3 and palavra not in palavras_irrelevantes
        ]
        
        return palavras_chave[:10]  # Limitar a 10 palavras-chave
    
    def _generate_cache_key(self, pergunta: str, area_juridica: str) -> str:
        """Gera chave única para cache"""
        content = f"{pergunta}_{area_juridica}"
        return hashlib.md5(content.encode()).hexdigest()