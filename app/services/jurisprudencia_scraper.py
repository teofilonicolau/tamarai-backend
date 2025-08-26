# app/services/jurisprudencia_scraper.py
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict

class JurisprudenciaScraper:
    
    async def buscar_stj_real(self, termo: str, area: str) -> List[Dict]:
        """Busca real no site do STJ"""
        url = "https://www.stj.jus.br/SCON/jurisprudencia/toc.jsp"
        
        async with aiohttp.ClientSession() as session:
            params = {
                'livre': termo,
                'b': 'ACOR',
                'thesaurus': 'JURIDICO'
            }
            
            async with session.get(url, params=params) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                resultados = []
                for item in soup.find_all('div', class_='jurisprudenciaResult'):
                    numero = item.find('span', class_='numeroAcordao')
                    ementa = item.find('div', class_='ementa')
                    
                    if numero and ementa:
                        resultados.append({
                            'tribunal': 'STJ',
                            'numero': numero.text.strip(),
                            'ementa': ementa.text.strip()[:500],
                            'url': f"https://www.stj.jus.br{item.find('a')['href']}"
                        })
                
                return resultados[:5]
    
    async def buscar_tst_trabalhista(self, termo: str) -> List[Dict]:
        """Busca específica no TST para casos trabalhistas"""
        url = "https://jurisprudencia.tst.jus.br/consulta-unificada"
        
        # Implementar busca específica no TST
        # Similar ao STJ mas com parâmetros específicos do TST
        pass