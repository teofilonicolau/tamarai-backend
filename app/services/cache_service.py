# app/services/cache_service.py
import redis
import json
import hashlib
from typing import Optional, Any
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def get_ai_response(self, cache_key: str) -> Optional[str]:
        """Recupera resposta da IA do cache"""
        try:
            return self.redis_client.get(f"ai_response:{cache_key}")
        except Exception as e:
            print(f"Erro ao buscar cache: {e}")
            return None
    
    async def set_ai_response(self, cache_key: str, response: str, ttl: int = None) -> bool:
        """Salva resposta da IA no cache"""
        try:
            if ttl is None:
                ttl = settings.CACHE_TTL_AI_RESPONSE
            
            self.redis_client.setex(
                f"ai_response:{cache_key}", 
                ttl, 
                response
            )
            return True
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")
            return False
    
    async def get_jurisprudencia(self, area: str, palavras_chave: list) -> Optional[list]:
        """Recupera jurisprudência do cache"""
        try:
            cache_key = self._generate_jurisprudencia_key(area, palavras_chave)
            cached_data = self.redis_client.get(f"jurisprudencia:{cache_key}")
            
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            print(f"Erro ao buscar jurisprudência do cache: {e}")
            return None
    
    async def set_jurisprudencia(self, area: str, palavras_chave: list, data: list) -> bool:
        """Salva jurisprudência no cache"""
        try:
            cache_key = self._generate_jurisprudencia_key(area, palavras_chave)
            
            self.redis_client.setex(
                f"jurisprudencia:{cache_key}",
                settings.CACHE_TTL_JURISPRUDENCIA,
                json.dumps(data, ensure_ascii=False)
            )
            return True
        except Exception as e:
            print(f"Erro ao salvar jurisprudência no cache: {e}")
            return False
    
    async def get_legislacao(self, area: str, termo: str) -> Optional[list]:
        """Recupera legislação do cache"""
        try:
            cache_key = self._generate_legislacao_key(area, termo)
            cached_data = self.redis_client.get(f"legislacao:{cache_key}")
            
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            print(f"Erro ao buscar legislação do cache: {e}")
            return None
    
    async def set_legislacao(self, area: str, termo: str, data: list) -> bool:
        """Salva legislação no cache"""
        try:
            cache_key = self._generate_legislacao_key(area, termo)
            
            self.redis_client.setex(
                f"legislacao:{cache_key}",
                settings.CACHE_TTL_JURISPRUDENCIA,
                json.dumps(data, ensure_ascii=False)
            )
            return True
        except Exception as e:
            print(f"Erro ao salvar legislação no cache: {e}")
            return False
    
    def _generate_jurisprudencia_key(self, area: str, palavras_chave: list) -> str:
        """Gera chave única para jurisprudência"""
        content = f"{area}_{'_'.join(sorted(palavras_chave))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_legislacao_key(self, area: str, termo: str) -> str:
        """Gera chave única para legislação"""
        content = f"{area}_{termo}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def clear_cache(self, pattern: str = "*") -> bool:
        """Limpa cache por padrão"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
            return False
    
    async def get_cache_stats(self) -> dict:
        """Retorna estatísticas do cache"""
        try:
            info = self.redis_client.info()
            return {
                "total_keys": info.get("db0", {}).get("keys", 0),
                "memory_used": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0)
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas do cache: {e}")
            return {}