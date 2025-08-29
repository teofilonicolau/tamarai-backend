# app/modules/previdenciario/service.py - VERSÃO COMPLETA COM 10 PETIÇÕES
from typing import List
from .schemas import DadosPrevidenciarios
from app.services.ai_service import ai_service
from app.core.ethics import EthicsService

class PrevidenciarioService:
    
    async def gerar_peticao_aposentadoria_invalidez(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para aposentadoria por invalidez"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para aposentadoria
        por invalidez com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Tipo: {dados.tipo_beneficio}
        - DER: {dados.der}
        - Motivo da recusa: {dados.motivo_recusa}
        - CID: {dados.cid_principal or 'A definir'}
        
        HISTÓRICO DETALHADO:
        - Histórico laboral: {dados.historico_laboral or 'A informar'}
        - Atividade especial: {"Sim" if dados.atividade_especial else "Não"}
        - Exposição a agentes nocivos: {dados.exposicao_agentes_nocivos or 'Não informado'}
        - Informações médicas: {dados.informacoes_medicas or 'A detalhar'}
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (histórico laboral detalhado e exposição ocupacional)
        3. DO DIREITO (Lei 8.213/91 art. 42)
        4. DA JURISPRUDÊNCIA (precedente sobre incapacidade permanente)
        5. DOS PEDIDOS (incluir tutela antecipada)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "TNU, PEDILEF 5001306-23.2014.4.04.7108/RS, Rel. Juiz Federal José Antonio Savaris, 
        que consolidou o entendimento sobre incapacidade laboral permanente"
        
        INCAPACIDADE PERMANENTE:
        Argumentar: "A aposentadoria por invalidez exige incapacidade total e permanente para 
        qualquer atividade laborativa, conforme art. 42 da Lei 8.213/91."
        
        TUTELA ANTECIPADA:
        Incluir: "A natureza alimentar do benefício e a comprovação médica da incapacidade 
        justificam a concessão da tutela antecipada."
        
        CÁLCULO E PLANILHA:
        Incluir: "O valor da RMI e das parcelas vencidas será demonstrado em planilha anexa, 
        considerando a integralidade do salário de benefício."
        
        DOCUMENTOS ESPECÍFICOS:
        {', '.join(dados.laudos_medicos) if dados.laudos_medicos else 'Laudos médicos a anexar'}
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao
    
    async def gerar_peticao_revisao_vida_toda(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para Revisão da Vida Toda"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para Revisão da Vida Toda
        com base na decisão do STF (RE 1.276.977) e os seguintes dados:
        
        DADOS DO CASO:
        - Benefício: {dados.numero_beneficio or 'A informar'}
        - DIB: {dados.dib or 'A informar'}
        - Tempo de contribuição: {dados.tempo_contribuicao_total or 0} meses
        - Histórico contributivo: {dados.historico_contribuicoes or 'A detalhar'}
        
        FUNDAMENTOS ESPECÍFICOS:
        - STF RE 1.276.977 (repercussão geral)
        - Inclusão de salários anteriores a julho/1994
        - Cálculo mais benéfico ao segurado
        - Prescrição quinquenal das parcelas
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (histórico contributivo pré-1994)
        3. DO DIREITO (STF RE 1.276.977)
        4. DA JURISPRUDÊNCIA (precedente específico)
        5. DOS PEDIDOS
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STF, RE 1.276.977, Rel. Ministro LUIZ FUX, que decidiu pela possibilidade 
        de inclusão dos salários anteriores a julho/1994 no cálculo do benefício"
        
        VALIDAÇÃO OBRIGATÓRIA:
        Incluir: "Conforme simulação técnica anexa, a inclusão das contribuições anteriores a julho/1994 
        resulta em um aumento significativo do benefício, comprovando ser a opção mais vantajosa ao segurado, 
        considerando os salários relevantes do período pré-Plano Real."
        
        PRESCRIÇÃO QUINQUENAL:
        Mencionar: "Aplica-se a prescrição quinquenal apenas às parcelas vencidas, 
        não ao direito à revisão do benefício."
        
        CÁLCULO COMPARATIVO:
        Incluir: "A planilha anexa demonstra o cálculo comparativo entre a regra atual 
        e a Revisão da Vida Toda, evidenciando a vantagem da revisão."
        
        HISTÓRICO CONTRIBUTIVO:
        Detalhar que o segurado possui contribuições desde {dados.historico_laboral or '1988'} com salários 
        expressivos antes de 1994.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_aposentadoria_tempo_contribuicao(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para aposentadoria por tempo de contribuição"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para aposentadoria
        por tempo de contribuição com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Tempo total: {dados.tempo_contribuicao_total or 0} meses ({(dados.tempo_contribuicao_total or 0) // 12} anos)
        - DER: {dados.der}
        - Motivo da recusa: {dados.motivo_recusa}
        - Histórico contributivo: {dados.historico_contribuicoes or 'A detalhar'}
        
        REQUISITOS LEGAIS:
        - Homem: 35 anos de contribuição (420 meses)
        - Mulher: 30 anos de contribuição (360 meses)
        - Carência: 180 contribuições mensais
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (histórico contributivo detalhado)
        3. DO DIREITO (Lei 8.213/91 arts. 52 e 53)
        4. DA JURISPRUDÊNCIA (incluir precedente específico do STJ sobre tempo de contribuição)
        5. DOS PEDIDOS (incluir tutela antecipada se aplicável)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, AgInt no REsp 1664845/SP, Rel. Ministro HERMAN BENJAMIN, que consolidou 
        o entendimento sobre a contagem integral do tempo de contribuição"
        
        CÁLCULO E PLANILHA:
        Incluir: "O valor da causa e os cálculos detalhados serão apresentados em planilha 
        técnica anexa, elaborada conforme metodologia do INSS e jurisprudência consolidada."
        
        Use jurisprudência específica do STJ sobre tempo de contribuição e CNIS.
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_auxilio_doenca(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para auxílio-doença"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para auxílio-doença
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - DER: {dados.der}
        - CID: {dados.cid_principal or 'A definir'}
        - Motivo da recusa: {dados.motivo_recusa}
        - Informações médicas: {dados.informacoes_medicas or 'A detalhar'}
        
        REQUISITOS LEGAIS:
        - Incapacidade temporária para o trabalho
        - Carência: 12 contribuições mensais
        - Qualidade de segurado
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (histórico médico e laboral)
        3. DO DIREITO (Lei 8.213/91 art. 59)
        4. DA JURISPRUDÊNCIA (precedente específico sobre incapacidade temporária)
        5. DOS PEDIDOS (incluir tutela antecipada OBRIGATÓRIA)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "TNU, PEDILEF 5001306-23.2014.4.04.7108/RS, que consolidou o entendimento 
        sobre a prevalência da prova pericial judicial sobre o laudo administrativo do INSS"
        
        ARGUMENTAÇÃO ESPECÍFICA:
        Incluir: "O laudo do perito do INSS tem caráter meramente administrativo, sendo a 
        prova pericial em juízo a mais relevante para aferição da incapacidade laboral."
        
        TUTELA ANTECIPADA:
        Argumentar: "A natureza alimentar do benefício e a verossimilhança das alegações 
        justificam a concessão da tutela antecipada."
        
        CÁLCULO E PLANILHA:
        Incluir: "O valor das parcelas vencidas e vincendas será demonstrado em planilha 
        técnica anexa, considerando a DER e o salário de benefício aplicável."
        
        DOCUMENTOS MÉDICOS:
        {', '.join(dados.laudos_medicos) if dados.laudos_medicos else 'Laudos médicos a anexar'}
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_pensao_morte(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para pensão por morte"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para pensão por morte
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Data do óbito: {dados.der}
        - Motivo da recusa: {dados.motivo_recusa}
        - Grau de parentesco: {dados.historico_laboral or 'A informar'}
        - Dependência econômica: {dados.informacoes_medicas or 'A comprovar'}
        
        REQUISITOS LEGAIS:
        - Qualidade de segurado do instituidor
        - Dependência econômica (quando aplicável)
        - Carência dispensada para pensão por morte
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES (incluir dados do falecido)
        2. DOS FATOS (óbito e dependência econômica)
        3. DO DIREITO (Lei 8.213/91 art. 74)
        4. DA JURISPRUDÊNCIA (precedente sobre dependência econômica)
        5. DOS PEDIDOS
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, AgRg no REsp 1360420/SP, Rel. Ministro HERMAN BENJAMIN, que consolidou 
        o entendimento sobre a presunção de dependência econômica do cônjuge"
        
        ARGUMENTAÇÃO ESPECÍFICA:
        Incluir: "A dependência econômica do cônjuge é presumida por lei, independentemente 
        de prova, conforme art. 16, I da Lei 8.213/91."
        
        CARÊNCIA DISPENSADA:
        Mencionar: "Para pensão por morte, a carência é dispensada, sendo necessária apenas 
        a qualidade de segurado do instituidor na data do óbito."
        
        CÁLCULO E PLANILHA:
        Incluir: "O valor do benefício e das parcelas vencidas será demonstrado em planilha 
        anexa, considerando a data do óbito como DIB."
        
        DOCUMENTOS ESSENCIAIS:
        - Certidão de óbito
        - Comprovação de dependência (quando aplicável)
        - CNIS do instituidor
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_aposentadoria_especial(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para aposentadoria especial"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para aposentadoria especial
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Tempo especial: {dados.tempo_contribuicao_total or 0} meses ({(dados.tempo_contribuicao_total or 0) // 12} anos)
        - Atividade especial: {"Sim" if dados.atividade_especial else "Não"}
        - Agentes nocivos: {dados.exposicao_agentes_nocivos or 'A especificar'}
        - DER: {dados.der}
        
        REQUISITOS LEGAIS:
        - 15, 20 ou 25 anos conforme agente nocivo
        - Exposição habitual e permanente
        - Comprovação através de PPP/LTCAT
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (exposição detalhada a agentes nocivos)
        3. DO DIREITO (Lei 8.213/91 art. 57 e EC 103/2019)
        4. DA JURISPRUDÊNCIA (precedente sobre atividade especial)
        5. DOS PEDIDOS
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, AgInt no REsp 1751363/PR, Rel. Ministro NAPOLEÃO NUNES MAIA FILHO, 
        sobre exposição habitual e permanente a agentes nocivos"
        
        REGRAS DE TRANSIÇÃO:
        Mencionar: "A EC 103/2019 manteve a previsão de aposentadoria especial, aplicando-se 
        as regras de transição quando aplicável ao caso concreto."
        
        CONVERSÃO DE TEMPO:
        Incluir: "Subsidiariamente, requer-se a conversão do tempo especial em comum para 
        fins de aposentadoria por tempo de contribuição."
        
        CÁLCULO E PLANILHA:
        Incluir: "O cálculo da RMI e a conversão do tempo especial serão demonstrados em 
        planilha técnica anexa, conforme metodologia consolidada."
        
        DOCUMENTOS ESPECÍFICOS:
        - PPP (Perfil Profissiográfico Previdenciário)
        - LTCAT (Laudo Técnico das Condições do Ambiente de Trabalho)
        - CTPS com anotações especiais
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_bpc_loas(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para BPC-LOAS"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para BPC-LOAS
        com base na Lei 8.742/93 (LOAS) e os seguintes dados:
        
        DADOS DO CASO:
        - Tipo: {dados.tipo_beneficio}
        - CID: {dados.cid_principal or 'A definir'}
        - Renda familiar: {dados.informacoes_medicas or 'A comprovar'}
        - Motivo da recusa: {dados.motivo_recusa}
        
        REQUISITOS LEGAIS:
        - Pessoa com deficiência ou idoso (65+ anos)
        - Renda familiar per capita inferior a 1/4 do salário mínimo
        - Não recebimento de outro benefício
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (deficiência detalhada e miserabilidade)
        3. DO DIREITO (Lei 8.742/93 art. 20)
        4. DA JURISPRUDÊNCIA (precedente do STF sobre miserabilidade)
        5. DOS PEDIDOS (incluir tutela antecipada OBRIGATÓRIA)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STF, RE 567.985/MT, que decidiu que o critério de 1/4 do salário mínimo 
        não é absoluto para aferição da miserabilidade"
        
        ARGUMENTAÇÃO ESPECÍFICA:
        Incluir: "A deficiência deve ser avaliada sob o aspecto biopsicossocial, conforme 
        Estatuto da Pessoa com Deficiência (Lei 13.146/2015)."
        
        TUTELA ANTECIPADA:
        Argumentar: "A natureza assistencial do benefício e a situação de vulnerabilidade 
        justificam a concessão da tutela antecipada."
        
        VALOR FIXO:
        Mencionar: "O BPC-LOAS corresponde a 1 salário mínimo mensal, não sendo necessário 
        cálculo complexo, apenas a contagem das parcelas vencidas."
        
        DOCUMENTOS MÉDICOS:
        {', '.join(dados.laudos_medicos) if dados.laudos_medicos else 'Laudos médicos a anexar'}
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_aposentadoria_rural(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para aposentadoria híbrida/rural"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para aposentadoria híbrida/rural
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Tempo rural: {dados.historico_laboral or 'A comprovar'}
        - Tempo urbano: {dados.tempo_contribuicao_total or 0} meses
        - DER: {dados.der}
        - Atividade rural: {dados.exposicao_agentes_nocivos or 'A detalhar'}
        
        REQUISITOS LEGAIS:
        - Somatória de tempo rural + urbano
        - Comprovação de atividade rural
        - Carência conforme período
        - Idade mínima: 60 anos (homem) / 55 anos (mulher)
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (atividade rural e urbana detalhada)
        3. DO DIREITO (Lei 8.213/91 art. 48, § 3º)
        4. DA JURISPRUDÊNCIA (precedente sobre aposentadoria híbrida)
        5. DOS PEDIDOS (incluir prova testemunhal)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, REsp 1.410.057/PR, que consolidou o entendimento sobre aposentadoria 
        híbrida mesmo sem atividade rural atual"
        
        PROVA TESTEMUNHAL:
        Incluir: "Requer-se a produção de prova testemunhal para comprovação da atividade 
        rural, conforme entendimento consolidado dos tribunais."
        
        IDADE MÍNIMA:
        Mencionar: "O requerente atende ao requisito etário para aposentadoria rural, 
        devendo ser observada a idade na DER."
        
        CÁLCULO E PLANILHA:
        Incluir: "A somatória dos períodos rural e urbano será demonstrada em planilha 
        anexa, comprovando o cumprimento dos requisitos legais."
        
        DOCUMENTOS RURAIS:
        - Declaração de aptidão ao PRONAF
        - Contratos de arrendamento
        - Notas fiscais de venda de produção
        - Comprovantes de ITR
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_salario_maternidade(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para salário-maternidade"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para salário-maternidade
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Data do parto/adoção: {dados.der}
        - Motivo da recusa: {dados.motivo_recusa}
        - Tipo: {dados.tipo_beneficio}
        - Carência: {dados.tempo_contribuicao_total or 0} meses
        
        REQUISITOS LEGAIS:
        - Qualidade de segurada
        - Carência: 10 contribuições (exceto acidente)
        - Período: 120 dias (parto) ou conforme idade (adoção)
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (parto/adoção e carência)
        3. DO DIREITO (Lei 8.213/91 art. 71)
        4. DA JURISPRUDÊNCIA (precedente sobre salário-maternidade)
        5. DOS PEDIDOS (incluir tutela antecipada OBRIGATÓRIA)
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, REsp 1.704.520, que consolidou o entendimento sobre a qualidade 
        de segurada como único requisito para salário-maternidade"
        
        ATIVIDADE RURAL:
        Se aplicável, mencionar: "Para segurada especial (rural), a comprovação da atividade 
        rural dispensa a carência de 10 meses."
        
        TUTELA ANTECIPADA:
        Argumentar: "A natureza alimentar do benefício e a necessidade de cuidados com o 
        recém-nascido justificam a concessão da tutela antecipada."
        
        CÁLCULO E PLANILHA:
        Incluir: "O valor do salário-maternidade e das parcelas será demonstrado em planilha 
        anexa, considerando o período de 120 dias e a RMI aplicável."
        
        DOCUMENTOS ESSENCIAIS:
        - Certidão de nascimento ou termo de adoção
        - Atestado médico
        - CNIS da segurada
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao

    async def gerar_peticao_revisao_beneficio(self, dados: DadosPrevidenciarios) -> str:
        """Gera petição para revisão de benefício (genérica)"""
        prompt = f"""
        Como especialista em Direito Previdenciário, elabore uma petição inicial para revisão de benefício
        com base na Lei 8.213/91 e os seguintes dados:
        
        DADOS DO CASO:
        - Benefício: {dados.numero_beneficio or 'A informar'}
        - DIB: {dados.dib or 'A informar'}
        - Motivo da revisão: {dados.motivo_recusa}
        - Tipo de revisão: {dados.tipo_beneficio}
        
        FUNDAMENTOS PARA REVISÃO:
        - Erro de cálculo na RMI
        - Não consideração de períodos contributivos
        - Aplicação incorreta de índices
        - Desconsideração de salários de contribuição
        
        ESTRUTURA OBRIGATÓRIA:
        1. QUALIFICAÇÃO DAS PARTES
        2. DOS FATOS (erro no cálculo original detalhado)
        3. DO DIREITO (Lei 8.213/91 art. 29)
        4. DA JURISPRUDÊNCIA (precedente sobre revisão)
        5. DOS PEDIDOS
        6. DO VALOR DA CAUSA
        
        JURISPRUDÊNCIA OBRIGATÓRIA:
        Citar: "STJ, REsp 1.310.034/SP, que consolidou o entendimento sobre a possibilidade 
        de revisão de benefícios quando comprovado erro de cálculo"
        
        PRESCRIÇÃO QUINQUENAL:
        Mencionar: "Aplica-se a prescrição quinquenal apenas às parcelas vencidas, 
        não ao direito à revisão do benefício."
        
        ERRO DE CÁLCULO:
        Detalhar: "O erro no cálculo da RMI resulta em prejuízo mensal ao segurado, 
        justificando a revisão para aplicação da metodologia correta."
        
        CÁLCULO E PLANILHA:
        Incluir: "A memória de cálculo correta será apresentada em planilha anexa, 
        demonstrando o valor devido e as diferenças a serem pagas."
        
        DOCUMENTOS NECESSÁRIOS:
        - Carta de concessão original
        - CNIS atualizado
        - Memória de cálculo correta
        """
        
        resultado = await ai_service.gerar_peticao_especializada(prompt, "previdenciario")
        peticao = resultado.get("peticao", "Erro ao gerar petição")
        peticao += f"\n\n{EthicsService.get_disclaimer()}"
        
        return peticao