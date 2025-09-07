# app/api/routes/analytics.py
from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime

router = APIRouter(prefix="/analytics")  # ← ADICIONAR ESTA LINHA

@router.get("/dashboard")
async def get_dashboard_metrics() -> Dict[str, Any]:
    """Métricas do dashboard executivo - MOCK DATA"""
    
    # Dados simulados para testar a interface
    return {
        "total_calculos": 127,
        "calculos_por_tipo": {
            "ec103": 45,
            "trabalhista": 32,
            "valor_causa": 28,
            "tempo_especial": 22
        },
        "feedback_medio": 4.3,
        "casos_mes": 38,
        "ultima_atualizacao": datetime.now().isoformat()
    }

@router.get("/metricas-detalhadas")
async def get_metricas_detalhadas():
    """Métricas detalhadas para análise - MOCK DATA"""
    
    return {
        "calculos_ultima_semana": 23,
        "tipos_mais_populares": [
            {"tipo": "ec103", "quantidade": 45},
            {"tipo": "trabalhista", "quantidade": 32},
            {"tipo": "valor_causa", "quantidade": 28},
            {"tipo": "tempo_especial", "quantidade": 22},
            {"tipo": "periodo_graca", "quantidade": 15}
        ],
        "crescimento_semanal": "+18%",
        "horario_pico": "14:00-16:00"
    }

@router.get("/status")
async def get_analytics_status():
    """Status do sistema de analytics"""
    return {
        "status": "operacional",
        "versao": "1.0.0",
        "banco_dados": "mock_data",
        "ultima_coleta": datetime.now().isoformat()
    }