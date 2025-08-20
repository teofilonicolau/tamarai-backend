# app/api/routes/peticoes.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os  # ← ADICIONADO PARA SUPORTE À EXCLUSÃO DE ARQUIVOS
from app.core.database import get_db
from app.core.dependencies import get_ai_service
from app.schemas.peticao import PeticaoCreate, PeticaoResponse, PeticaoAprovacao
from app.models.peticao import Peticao, StatusPeticao
from app.services.ai_service import AIService
from app.services.pdf_service import PDFService

router = APIRouter()

@router.post("/", response_model=PeticaoResponse)
async def criar_peticao(
    peticao: PeticaoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Cria uma nova petição e gera o texto com IA"""
    try:
        dados_dict = {
            "titulo": peticao.titulo,
            "tipo": peticao.tipo.value,
            "area_juridica": peticao.area_juridica.value,
            "dados_autor": peticao.dados_autor.dict(),
            "dados_especificos": peticao.dados_especificos,
            "pedidos": peticao.pedidos.dict(),
            "documentos_anexos": peticao.documentos_anexos
        }

        db_peticao = Peticao(
            titulo=peticao.titulo,
            tipo=peticao.tipo,
            area_juridica=peticao.area_juridica,
            status=StatusPeticao.RASCUNHO,
            dados_formulario=dados_dict
        )

        db.add(db_peticao)
        db.commit()
        db.refresh(db_peticao)

        background_tasks.add_task(
            gerar_peticao_background,
            db_peticao.id,
            dados_dict,
            peticao.area_juridica.value
        )

        return db_peticao

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar petição: {str(e)}"
        )

async def gerar_peticao_background(peticao_id: int, dados_dict: dict, area_juridica: str):
    """Gera o texto da petição em background"""
    from app.core.database import SessionLocal

    db = SessionLocal()
    ai_service = AIService()
    pdf_service = PDFService()

    try:
        peticao = db.query(Peticao).filter(Peticao.id == peticao_id).first()
        if not peticao:
            return

        resultado_ia = await ai_service.gerar_peticao(dados_dict, area_juridica)

        pdf_path = await pdf_service.gerar_peticao_pdf(
            dados_dict,
            resultado_ia["texto_peticao"],
            f"peticao_{peticao_id}.pdf"
        )

        peticao.texto_gerado = resultado_ia["texto_peticao"]
        peticao.pdf_path = pdf_path
        peticao.jurisprudencia_utilizada = resultado_ia.get("jurisprudencia_utilizada", [])
        peticao.legislacao_aplicada = resultado_ia.get("legislacao_aplicada", [])
        peticao.prompt_utilizado = resultado_ia.get("prompt_utilizado", "")
        peticao.status = StatusPeticao.GERADA

        db.commit()

    except Exception as e:
        print(f"Erro ao gerar petição em background: {e}")
        if peticao:
            peticao.status = StatusPeticao.RASCUNHO
            db.commit()
    finally:
        db.close()

@router.get("/", response_model=List[PeticaoResponse])
async def listar_peticoes(
    skip: int = 0,
    limit: int = 100,
    area_juridica: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Lista petições com filtros opcionais"""
    query = db.query(Peticao)

    if area_juridica:
        query = query.filter(Peticao.area_juridica == area_juridica)

    if status:
        query = query.filter(Peticao.status == status)

    peticoes = query.offset(skip).limit(limit).order_by(Peticao.created_at.desc()).all()
    return peticoes

@router.get("/{peticao_id}", response_model=PeticaoResponse)
async def obter_peticao(
    peticao_id: int,
    db: Session = Depends(get_db)
):
    """Obtém uma petição específica"""
    peticao = db.query(Peticao).filter(Peticao.id == peticao_id).first()

    if not peticao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petição não encontrada"
        )

    return peticao

@router.post("/{peticao_id}/aprovar")
async def aprovar_peticao(
    peticao_id: int,
    aprovacao: PeticaoAprovacao,
    db: Session = Depends(get_db)
):
    """Aprova ou rejeita uma petição"""
    peticao = db.query(Peticao).filter(Peticao.id == peticao_id).first()

    if not peticao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petição não encontrada"
        )

    if peticao.status != StatusPeticao.GERADA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Petição deve estar no status 'gerada' para ser aprovada"
        )

    peticao.aprovado_por_humano = aprovacao.aprovado
    peticao.observacoes_aprovacao = aprovacao.observacoes
    peticao.status = StatusPeticao.APROVADA if aprovacao.aprovado else StatusPeticao.RASCUNHO
    peticao.approved_at = db.func.now() if aprovacao.aprovado else None

    db.commit()

    return {
        "message": "Petição aprovada com sucesso" if aprovacao.aprovado else "Petição rejeitada",
        "status": peticao.status
    }

@router.get("/{peticao_id}/status")
async def verificar_status_peticao(
    peticao_id: int,
    db: Session = Depends(get_db)
):
    """Verifica o status de geração de uma petição"""
    peticao = db.query(Peticao).filter(Peticao.id == peticao_id).first()

    if not peticao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petição não encontrada"
        )

    return {
        "id": peticao.id,
        "status": peticao.status,
        "texto_gerado": bool(peticao.texto_gerado),
        "pdf_disponivel": bool(peticao.pdf_path),
        "aprovado": peticao.aprovado_por_humano
    }

@router.delete("/{peticao_id}")
async def deletar_peticao(
    peticao_id: int,
    db: Session = Depends(get_db)
):
    """Deleta uma petição"""
    peticao = db.query(Peticao).filter(Peticao.id == peticao_id).first()

    if not peticao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petição não encontrada"
        )

    if peticao.pdf_path and os.path.exists(peticao.pdf_path):
        os.remove(peticao.pdf_path)

    db.delete(peticao)
    db.commit()

    return {"message": "Petição deletada com sucesso"}
