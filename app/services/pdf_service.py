# app/services/pdf_service.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from typing import Dict, Any, Optional
import os
from datetime import datetime
from app.core.config import settings

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para petições jurídicas"""
        
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Title'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Times-Bold'
        ))
        
        # Estilo para seções
        self.styles.add(ParagraphStyle(
            name='Secao',
            parent=self.styles['Heading1'],
            fontSize=12,
            spaceAfter=12,
            spaceBefore=12,
            alignment=TA_CENTER,
            fontName='Times-Bold'
        ))
        
        # Estilo para texto jurídico
        self.styles.add(ParagraphStyle(
            name='TextoJuridico',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman',
            leading=18  # Espaçamento 1.5
        ))
        
        # Estilo para qualificação
        self.styles.add(ParagraphStyle(
            name='Qualificacao',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Times-Roman',
            leftIndent=2*cm
        ))
        
        # Estilo para assinatura
        self.styles.add(ParagraphStyle(
            name='Assinatura',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Times-Roman'
        ))
    
    async def gerar_peticao_pdf(
        self, 
        dados_peticao: Dict[str, Any], 
        texto_peticao: str,
        nome_arquivo: Optional[str] = None
    ) -> str:
        """Gera PDF da petição com formatação jurídica"""
        
        if not nome_arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"peticao_{timestamp}.pdf"
        
        # Caminho completo do arquivo
        pdf_path = os.path.join(settings.PDF_OUTPUT_DIR, nome_arquivo)
        
        # Criar documento PDF
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Construir conteúdo
        story = []
        
        # Cabeçalho
        story.extend(self._criar_cabecalho(dados_peticao))
        
        # Corpo da petição
        story.extend(self._processar_texto_peticao(texto_peticao))
        
        # Rodapé
        story.extend(self._criar_rodape(dados_peticao))
        
        # Gerar PDF
        doc.build(story)
        
        return pdf_path
    
    def _criar_cabecalho(self, dados_peticao: Dict[str, Any]) -> list:
        """Cria cabeçalho da petição"""
        elementos = []
        
        # Logo do escritório (se existir)
        logo_path = os.path.join(settings.STATIC_DIR, "logo_escritorio.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=3*cm, height=2*cm)
            logo.hAlign = 'CENTER'
            elementos.append(logo)
            elementos.append(Spacer(1, 0.5*cm))
        
        # Título do documento
        titulo = dados_peticao.get('titulo', 'PETIÇÃO INICIAL')
        elementos.append(Paragraph(titulo.upper(), self.styles['TituloPrincipal']))
        elementos.append(Spacer(1, 0.5*cm))
        
        return elementos
    
    def _processar_texto_peticao(self, texto_peticao: str) -> list:
        """Processa e formata o texto da petição"""
        elementos = []
        
        # Dividir texto em seções
        secoes = self._dividir_em_secoes(texto_peticao)
        
        for secao in secoes:
            if secao['tipo'] == 'titulo':
                elementos.append(Paragraph(secao['conteudo'], self.styles['Secao']))
            elif secao['tipo'] == 'paragrafo':
                elementos.append(Paragraph(secao['conteudo'], self.styles['TextoJuridico']))
            elif secao['tipo'] == 'qualificacao':
                elementos.append(Paragraph(secao['conteudo'], self.styles['Qualificacao']))
            
            elementos.append(Spacer(1, 0.3*cm))
        
        return elementos
    
    def _dividir_em_secoes(self, texto: str) -> list:
        """Divide o texto em seções identificando títulos e parágrafos"""
        linhas = texto.split('\n')
        secoes = []
        
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            
            # Identificar títulos (texto em maiúsculo ou com padrões específicos)
            if (linha.isupper() or 
                linha.startswith('EXCELENTÍSSIMO') or
                linha.startswith('DOS ') or
                linha.startswith('DA ') or
                linha.startswith('DO ')):
                secoes.append({
                    'tipo': 'titulo',
                    'conteudo': linha
                })
            # Identificar qualificação (linhas com dados pessoais)
            elif any(palavra in linha.lower() for palavra in ['cpf', 'rg', 'endereço', 'brasileiro']):
                secoes.append({
                    'tipo': 'qualificacao',
                    'conteudo': linha
                })
            else:
                secoes.append({
                    'tipo': 'paragrafo',
                    'conteudo': linha
                })
        
        return secoes
    
    def _criar_rodape(self, dados_peticao: Dict[str, Any]) -> list:
        """Cria rodapé da petição"""
        elementos = []
        
        # Espaçamento
        elementos.append(Spacer(1, 1*cm))
        
        # Local e data
        hoje = datetime.now()
        local_data = f"São Paulo, {hoje.day} de {self._mes_por_extenso(hoje.month)} de {hoje.year}."
        elementos.append(Paragraph(local_data, self.styles['Assinatura']))
        elementos.append(Spacer(1, 1*cm))
        
        # Assinatura do advogado
        nome_advogado = dados_peticao.get('dados_autor', {}).get('nome_advogado', 'Dr. Rian Nicolau')
        oab = dados_peticao.get('dados_autor', {}).get('oab', 'OAB/SP 123.456')
        
        elementos.append(Paragraph("_" * 40, self.styles['Assinatura']))
        elementos.append(Paragraph(f"<b>{nome_advogado}</b>", self.styles['Assinatura']))
        elementos.append(Paragraph(oab, self.styles['Assinatura']))
        
        return elementos
    
    def _mes_por_extenso(self, mes: int) -> str:
        """Converte número do mês para nome por extenso"""
        meses = [
            '', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
        ]
        return meses[mes]
    
    async def gerar_relatorio_consulta(self, consulta_data: Dict[str, Any]) -> str:
        """Gera relatório PDF de uma consulta jurídica"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"consulta_{timestamp}.pdf"
        pdf_path = os.path.join(settings.PDF_OUTPUT_DIR, nome_arquivo)
        
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Título
        story.append(Paragraph("RELATÓRIO DE CONSULTA JURÍDICA", self.styles['TituloPrincipal']))
        story.append(Spacer(1, 0.5*cm))
        
        # Dados da consulta
        story.append(Paragraph("<b>Área Jurídica:</b> " + consulta_data.get('area_juridica', '').title(), self.styles['TextoJuridico']))
        story.append(Paragraph("<b>Data:</b> " + datetime.now().strftime("%d/%m/%Y %H:%M"), self.styles['TextoJuridico']))
        story.append(Spacer(1, 0.5*cm))
        
        # Pergunta
        story.append(Paragraph("CONSULTA:", self.styles['Secao']))
        story.append(Paragraph(consulta_data.get('pergunta', ''), self.styles['TextoJuridico']))
        story.append(Spacer(1, 0.5*cm))
        
        # Resposta
        story.append(Paragraph("RESPOSTA:", self.styles['Secao']))
        story.append(Paragraph(consulta_data.get('resposta', ''), self.styles['TextoJuridico']))
        
        # Jurisprudência utilizada
        if consulta_data.get('jurisprudencia_utilizada'):
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph("JURISPRUDÊNCIA CONSULTADA:", self.styles['Secao']))
            for jurisp in consulta_data['jurisprudencia_utilizada']:
                story.append(Paragraph(f"• {jurisp.get('numero', '')} - {jurisp.get('ementa', '')}", self.styles['TextoJuridico']))
        
        doc.build(story)
        return pdf_path