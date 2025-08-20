# app/api/routes/consultas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_ai_service
from app.schemas.consulta import ConsultaCreate, ConsultaResponse, ConsultaEspecializada
from app.models.consulta import Consulta
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/", response_model=ConsultaResponse)
async def criar_consulta(
    consulta: ConsultaCreate,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Cria uma nova consulta jurídica"""
    
    try:
        # Gerar resposta com IA
        resultado_ia = await ai_service.consulta_juridica_especializada(
            pergunta=consulta.pergunta,
            area_juridica=consulta.area_juridica.value,
            incluir_jurisprudencia=True,
            incluir_legislacao=True
        )
        
        # Salvar no banco
        db_consulta = Consulta(
            pergunta=consulta.pergunta,
            resposta=resultado_ia["resposta"],
            area_juridica=consulta.area_juridica,
            palavras_chave=resultado_ia.get("palavras_chave", []),
            jurisprudencia_utilizada=resultado_ia.get("jurisprudencia_utilizada", []),
            legislacao_aplicada=resultado_ia.get("legislacao_aplicada", []),
            tempo_resposta=resultado_ia.get("tempo_resposta", 0)
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

@router.post("/especializada", response_model=dict)
async def consulta_especializada(
    consulta: ConsultaEspecializada,
    ai_service: AIService = Depends(get_ai_service)
):
    """Consulta jurídica especializada sem salvar no banco"""
    
    try:
        # Determinar área jurídica automaticamente se não especificada
        area_juridica = "previdenciario"  # Default
        
        # Detectar área baseada em palavras-chave
        pergunta_lower = consulta.pergunta.lower()
        if any(palavra in pergunta_lower for palavra in ['inss', 'aposentadoria', 'auxílio', 'benefício', 'previdência']):
            area_juridica = "previdenciario"
        elif any(palavra in pergunta_lower for palavra in ['consumidor', 'produto', 'serviço', 'fornecedor', 'cdc']):
            area_juridica = "consumidor"
        elif any(palavra in pergunta_lower for palavra in ['processo', 'petição', 'recurso', 'cpc', 'procedimento']):
            area_juridica = "processual_civil"
        
        resultado = await ai_service.consulta_juridica_especializada(
            pergunta=consulta.pergunta,
            area_juridica=area_juridica,
            incluir_jurisprudencia=consulta.incluir_jurisprudencia,
            incluir_legislacao=consulta.incluir_legislacao
        )
        
        return {
            "resposta": resultado["resposta"],
            "area_detectada": area_juridica,
            "jurisprudencia": resultado.get("jurisprudencia_utilizada", []),
            "legislacao": resultado.get("legislacao_aplicada", []),
            "palavras_chave": resultado.get("palavras_chave", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar consulta especializada: {str(e)}"
        )

@router.get("/", response_model=List[ConsultaResponse])
async def listar_consultas(
    skip: int = 0,
    limit: int = 100,
    area_juridica: str = None,
    db: Session = Depends(get_db)
):
    """Lista consultas com filtros opcionais"""
    
    query = db.query(Consulta)
    
    if area_juridica:
        query = query.filter(Consulta.area_juridica == area_juridica)
    
    consultas = query.offset(skip).limit(limit).all()
    return consultas

@router.get("/{consulta_id}", response_model=ConsultaResponse)
async def obter_consulta(
    consulta_id: int,
    db: Session = Depends(get_db)
):
    """Obtém uma consulta específica"""
    
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada"
        )
    
    return consulta

@router.delete("/{consulta_id}")
async def deletar_consulta(
    consulta_id: int,
    db: Session = Depends(get_db)
):
    """Deleta uma consulta"""
    
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada"
        )
    
    db.delete(consulta)
    db.commit()
    
    return {"message": "Consulta deletada com sucesso"}

@router.post("/{consulta_id}/avaliar")
async def avaliar_consulta(
    consulta_id: int,
    satisfacao: int,
    db: Session = Depends(get_db)
):
    """Avalia a satisfação com uma consulta (1-5)"""
    
    if not 1 <= satisfacao <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Satisfação deve ser entre 1 e 5"
        )
    
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada"
        )
    
    consulta.satisfacao_usuario = satisfacao
    db.commit()
    
    return {"message": "Avaliação registrada com sucesso"}