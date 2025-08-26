# app/core/rate_limiter.py
from fastapi import Request, HTTPException
import redis
import time

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def check_rate_limit(self, request: Request, max_requests: int = 100, window: int = 3600):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        current = self.redis.get(key)
        if current is None:
            self.redis.setex(key, window, 1)
            return True
        
        if int(current) >= max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.redis.incr(key)
        return True