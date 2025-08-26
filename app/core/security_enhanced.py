# app/core/security_enhanced.py - CRIAR NOVO
from cryptography.fernet import Fernet
import os
import hashlib

class DataProtectionService:
    """Serviço para proteção de dados sensíveis"""
    
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher = Fernet(self.key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Criptografa dados sensíveis"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Descriptografa dados sensíveis"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def hash_user_data(self, data: str) -> str:
        """Gera hash para auditoria sem expor dados"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]

# Instância global
data_protection = DataProtectionService()