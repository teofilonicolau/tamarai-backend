# app/api/routes/consultas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_ai_service
from app.schemas.consulta import ConsultaCreate, ConsultaResponse
from app.models.consulta import Consulta
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/", response_model=ConsultaResponse)
async def criar_consulta(
    consulta: ConsultaCreate,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Criar uma nova consulta jurídica"""
    try:
        # Fazer consulta com IA
        resultado_ia = await ai_service.fazer_consulta_juridica(
            consulta.pergunta, 
            consulta.area_juridica.value
        )
        
        # Salvar no banco
        db_consulta = Consulta(
            pergunta=consulta.pergunta,
            resposta=resultado_ia.get("resposta", ""),
            area_juridica=consulta.area_juridica,
            tempo_resposta=resultado_ia.get("tokens_usados", 0)
        )
        
        db.add(db_consulta)
        db.commit()
        db.refresh(db_consulta)
        
        return db_consulta
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar consulta: {str(e)}"
        )

@router.get("/", response_model=List[ConsultaResponse])
async def listar_consultas(
    skip: int = 0,
    limit: int = 100,
    area_juridica: str = None,
    db: Session = Depends(get_db)
):
    """Listar consultas com filtros opcionais"""
    query = db.query(Consulta)
    
    if area_juridica:
        query = query.filter(Consulta.area_juridica == area_juridica)
    
    consultas = query.offset(skip).limit(limit).order_by(Consulta.created_at.desc()).all()
    return consultas

@router.get("/{consulta_id}", response_model=ConsultaResponse)
async def obter_consulta(
    consulta_id: int,
    db: Session = Depends(get_db)
):
    """Obter uma consulta específica"""
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada"
        )
    
    return consulta