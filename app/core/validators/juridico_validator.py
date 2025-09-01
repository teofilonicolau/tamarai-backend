# app/core/validators/juridico_validator.py
from datetime import date, timedelta
from typing import Dict, Any, Optional
import re

class ValidadorJuridico:
    
    def validar_datas(self, dib: date, der: date, eventos: dict) -> bool:
        """Evita erro: DIB ≠ data do parto"""
        # DIB não pode ser posterior à DER
        if dib > der:
            return False
        
        # Verificar consistência com eventos específicos
        if 'data_parto' in eventos:
            data_parto = eventos['data_parto']
            if isinstance(data_parto, str):
                # Converter string para date se necessário
                try:
                    data_parto = date.fromisoformat(data_parto)
                except:
                    return False
            
            # DIB deve coincidir com data do parto para salário-maternidade
            if abs((dib - data_parto).days) > 1:
                return False
        
        return True
        
    def calcular_periodo_graca(self, ultima_atividade: date, evento: date) -> bool:
        """Evita erro: 03/2022 → 07/2025 = período ultrapassado"""
        diferenca = evento - ultima_atividade
        
        # Período de graça máximo: 12 meses para segurado comum
        if diferenca.days > 365:
            return False
        
        return True
        
    def converter_tempo_especial(self, anos: int) -> int:
        """Evita erro: 27 anos → 27 meses"""
        if anos > 100:  # Provavelmente já está em meses
            return anos
        
        return anos * 12  # Converter anos para meses
        
    def classificar_segurado(self, historico: str) -> str:
        """Evita erro: rural pura vs híbrida"""
        historico_lower = historico.lower()
        
        # Verificar se tem atividade urbana
        termos_urbanos = ['carteira', 'clt', 'empresa', 'salário', 'contribuição']
        tem_urbano = any(termo in historico_lower for termo in termos_urbanos)
        
        # Verificar se tem atividade rural
        termos_rurais = ['rural', 'agricultura', 'fazenda', 'roça', 'campo']
        tem_rural = any(termo in historico_lower for termo in termos_rurais)
        
        if tem_rural and tem_urbano:
            return "hibrida"
        elif tem_rural:
            return "rural_pura"
        else:
            return "urbano"
    
    def validar_documentos_por_tipo_segurado(self, tipo_segurado: str, documentos: list) -> bool:
        """Valida documentos conforme tipo de segurado"""
        if tipo_segurado == "rural_pura":
            # Segurado especial não deve ter CNIS
            if any("cnis" in doc.lower() for doc in documentos):
                return False
        
        return True