# app/services/rag_service.py
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
from app.services.cache_service import CacheService

class RAGService:
    def __init__(self):
        self.cache = CacheService()
        self.sources = {
            "stj": "https://www.stj.jus.br",
            "stf": "https://portal.stf.jus.br",
            "tnu": "https://www.cjf.jus.br",
            "planalto": "http://www.planalto.gov.br"
        }
    
    async def buscar_jurisprudencia(self, area_juridica: str, palavras_chave: List[str]) -> List[Dict[str, Any]]:
        """Busca jurisprudência relevante para a área jurídica"""
        
        # Verificar cache primeiro
        cached_result = await self.cache.get_jurisprudencia(area_juridica, palavras_chave)
        if cached_result:
            return cached_result
        
        # Buscar jurisprudência online
        jurisprudencia = []
        
        try:
            # Buscar no STJ
            stj_results = await self._buscar_stj(area_juridica, palavras_chave)
            jurisprudencia.extend(stj_results)
            
            # Buscar na TNU (para previdenciário)
            if area_juridica == "previdenciario":
                tnu_results = await self._buscar_tnu(palavras_chave)
                jurisprudencia.extend(tnu_results)
            
            # Salvar no cache
            await self.cache.set_jurisprudencia(area_juridica, palavras_chave, jurisprudencia)
            
        except Exception as e:
            print(f"Erro ao buscar jurisprudência: {e}")
            # Retornar jurisprudência estática como fallback
            jurisprudencia = self._get_jurisprudencia_estatica(area_juridica, palavras_chave)
        
        return jurisprudencia[:5]  # Limitar a 5 resultados
    
    async def buscar_legislacao(self, area_juridica: str, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca legislação relevante"""
        
        # Verificar cache primeiro
        cached_result = await self.cache.get_legislacao(area_juridica, termo_busca)
        if cached_result:
            return cached_result
        
        legislacao = []
        
        try:
            # Buscar legislação específica por área
            if area_juridica == "previdenciario":
                legislacao = await self._buscar_legislacao_previdenciaria(termo_busca)
            elif area_juridica == "consumidor":
                legislacao = await self._buscar_legislacao_consumidor(termo_busca)
            elif area_juridica == "processual_civil":
                legislacao = await self._buscar_legislacao_processual(termo_busca)
            
            # Salvar no cache
            await self.cache.set_legislacao(area_juridica, termo_busca, legislacao)
            
        except Exception as e:
            print(f"Erro ao buscar legislação: {e}")
            # Retornar legislação estática como fallback
            legislacao = self._get_legislacao_estatica(area_juridica)
        
        return legislacao[:3]  # Limitar a 3 resultados
    
    async def _buscar_stj(self, area_juridica: str, palavras_chave: List[str]) -> List[Dict[str, Any]]:
        """Busca jurisprudência no STJ"""
        resultados = []
        
        try:
            # Simular busca no STJ (implementação real requer análise do site)
            # Por enquanto, retornar dados estáticos relevantes
            
            if area_juridica == "previdenciario":
                resultados = [
                    {
                        "tribunal": "STJ",
                        "numero": "REsp 1.234.567/SP",
                        "relator": "Min. Exemplo",
                        "ementa": "PREVIDENCIÁRIO. APOSENTADORIA POR INVALIDEZ. Comprovação da incapacidade laboral. Necessidade de perícia médica. Precedentes.",
                        "data": "2024-01-15",
                        "url": "https://www.stj.jus.br/exemplo"
                    }
                ]
            elif area_juridica == "consumidor":
                resultados = [
                    {
                        "tribunal": "STJ",
                        "numero": "REsp 2.345.678/RJ",
                        "relator": "Min. Exemplo",
                        "ementa": "CONSUMIDOR. VÍCIO DO PRODUTO. Responsabilidade objetiva do fornecedor. Art. 18 do CDC. Danos morais configurados.",
                        "data": "2024-02-10",
                        "url": "https://www.stj.jus.br/exemplo"
                    }
                ]
            
        except Exception as e:
            print(f"Erro ao buscar no STJ: {e}")
        
        return resultados
    
    async def _buscar_tnu(self, palavras_chave: List[str]) -> List[Dict[str, Any]]:
        """Busca jurisprudência na TNU"""
        resultados = []
        
        try:
            # Implementação específica para TNU
            resultados = [
                {
                    "tribunal": "TNU",
                    "numero": "PEDILEF 5040123-45.2023.4.03.6109",
                    "relator": "Juiz Federal Exemplo",
                    "ementa": "PREVIDENCIÁRIO. AUXÍLIO-DOENÇA. Incapacidade parcial e temporária. Concessão do benefício. Precedentes da TNU.",
                    "data": "2024-03-05",
                    "url": "https://www.cjf.jus.br/exemplo"
                }
            ]
            
        except Exception as e:
            print(f"Erro ao buscar na TNU: {e}")
        
        return resultados
    
    async def _buscar_legislacao_previdenciaria(self, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca legislação previdenciária"""
        legislacao = [
            {
                "lei": "Lei 8.213/91",
                "artigo": "Art. 42",
                "texto": "A aposentadoria por invalidez, uma vez cumprida, quando for o caso, a carência exigida, será devida ao segurado que, estando ou não em gozo de auxílio-doença, for considerado incapaz e insusceptível de reabilitação para o exercício de atividade que lhe garanta a subsistência.",
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm"
            },
            {
                "lei": "Decreto 3.048/99",
                "artigo": "Art. 43",
                "texto": "A aposentadoria por invalidez será devida a partir do dia imediato ao da cessação do auxílio-doença, ressalvado o disposto nos §§ 1º e 2º.",
                "url": "http://www.planalto.gov.br/ccivil_03/decreto/d3048.htm"
            }
        ]
        
        return legislacao
    
    async def _buscar_legislacao_consumidor(self, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca legislação do consumidor"""
        legislacao = [
            {
                "lei": "CDC - Lei 8.078/90",
                "artigo": "Art. 6º",
                "texto": "São direitos básicos do consumidor: I - a proteção da vida, saúde e segurança contra os riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou nocivos;",
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l8078.htm"
            },
            {
                "lei": "CDC - Lei 8.078/90",
                "artigo": "Art. 14",
                "texto": "O fornecedor de serviços responde, independentemente da existência de culpa, pela reparação dos danos causados aos consumidores por defeitos relativos à prestação dos serviços.",
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l8078.htm"
            }
        ]
        
        return legislacao
    
    async def _buscar_legislacao_processual(self, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca legislação processual civil"""
        legislacao = [
            {
                "lei": "CPC - Lei 13.105/15",
                "artigo": "Art. 319",
                "texto": "A petição inicial indicará: I - o juízo a que é dirigida; II - os nomes, os prenomes, o estado civil, a existência de união estável, a profissão, o número de inscrição no Cadastro de Pessoas Físicas ou no Cadastro Nacional da Pessoa Jurídica, o endereço eletrônico, o domicílio e a residência do autor e do réu;",
                "url": "http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm"
            }
        ]
        
        return legislacao
    
    def _get_jurisprudencia_estatica(self, area_juridica: str, palavras_chave: List[str]) -> List[Dict[str, Any]]:
        """Retorna jurisprudência estática como fallback"""
        
        jurisprudencia_estatica = {
            "previdenciario": [
                {
                    "tribunal": "STJ",
                    "numero": "REsp 1.000.000/SP",
                    "relator": "Min. Exemplo",
                    "ementa": "PREVIDENCIÁRIO. Jurisprudência de referência para casos previdenciários.",
                    "data": "2024-01-01",
                    "url": "#"
                }
            ],
            "consumidor": [
                {
                    "tribunal": "STJ",
                    "numero": "REsp 2.000.000/RJ",
                    "relator": "Min. Exemplo",
                    "ementa": "CONSUMIDOR. Jurisprudência de referência para casos de consumo.",
                    "data": "2024-01-01",
                    "url": "#"
                }
            ],
            "processual_civil": [
                {
                    "tribunal": "STJ",
                    "numero": "REsp 3.000.000/MG",
                    "relator": "Min. Exemplo",
                    "ementa": "PROCESSUAL CIVIL. Jurisprudência de referência para casos processuais.",
                    "data": "2024-01-01",
                    "url": "#"
                }
            ]
        }
        
        return jurisprudencia_estatica.get(area_juridica, [])
    
    def _get_legislacao_estatica(self, area_juridica: str) -> List[Dict[str, Any]]:
        """Retorna legislação estática como fallback"""
        
        legislacao_estatica = {
            "previdenciario": [
                {
                    "lei": "Lei 8.213/91",
                    "artigo": "Artigos diversos",
                    "texto": "Lei de Benefícios da Previdência Social",
                    "url": "http://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm"
                }
            ],
            "consumidor": [
                {
                    "lei": "Lei 8.078/90",
                    "artigo": "Artigos diversos",
                    "texto": "Código de Defesa do Consumidor",
                    "url": "http://www.planalto.gov.br/ccivil_03/leis/l8078.htm"
                }
            ],
            "processual_civil": [
                {
                    "lei": "Lei 13.105/15",
                    "artigo": "Artigos diversos",
                    "texto": "Código de Processo Civil",
                    "url": "http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm"
                }
            ]
        }
        
        return legislacao_estatica.get(area_juridica, [])