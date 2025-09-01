
<div align="center">

<img src="https://github.com/user-attachments/assets/c7886d0b-0262-4835-944b-19f3f1ce1d83?raw=true" alt="logoTamar" width="200"/>

# 🏛️ TamarAI Backend - IA Jurídica 

## **Inteligência Artificial especializada em simplificar sua vida**  
### Sistema completo para geração automática de petições jurídicas com qualidade profissional

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

---

## 🎯 **Funcionalidades Principais**

### 📋 **10 Tipos de Petições Previdenciárias**
- 🏥 **Aposentadoria por Invalidez** - Com análise médica especializada
- 🔄 **Revisão da Vida Toda** - Baseada no STF RE 1.276.977
- ⏰ **Aposentadoria por Tempo de Contribuição** - Regras de transição EC 103/2019
- 🏥 **Auxílio-Doença** - Com tutela antecipada automática
- 💔 **Pensão por Morte** - Análise de dependência econômica
- ⚠️ **Aposentadoria Especial** - Conversão de tempo especial
- 🤝 **BPC-LOAS** - Critério de miserabilidade flexibilizado
- 🌾 **Aposentadoria Rural/Híbrida** - Tempo rural + urbano
- 👶 **Salário-Maternidade** - Todas as modalidades
- 📊 **Revisão de Benefício** - Correção de cálculos

### 🤖 **IA Especializada**
- 🧠 **Persona jurídica especializada** em Direito Previdenciário
- ⚖️ **Jurisprudência atualizada** (STF, STJ, TNU, TRF5)
- 📝 **Preenchimento automático** de dados e placeholders
- 🎯 **Tutela antecipada** inserida automaticamente quando aplicável
- 💰 **Cálculo inteligente** do valor da causa

---

## 🚀 **Tecnologias & Frameworks**

### **Core Technologies**
![Python](https://img.shields.io/badge/Python-3.13-3776ab?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.10.4-e92063?logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32.1-4051b5?logo=uvicorn&logoColor=white)

### **AI & ML**
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai&logoColor=white)
![AI](https://img.shields.io/badge/Specialized-Legal%20AI-ff6b35?logo=artificial-intelligence&logoColor=white)

### **Database & Cache**
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-d71f00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-5.2.1-dc382d?logo=redis&logoColor=white)

### **Security & Auth**
![Passlib](https://img.shields.io/badge/Passlib-1.7.4-green?logo=security&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-45.0.6-blue?logo=security&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-3.3.0-000000?logo=json-web-tokens&logoColor=white)

### **Document Processing**
![ReportLab](https://img.shields.io/badge/ReportLab-4.2.5-orange?logo=adobe-acrobat-reader&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.12.3-yellow?logo=python&logoColor=white)

### **HTTP & Networking**
![HTTPX](https://img.shields.io/badge/HTTPX-0.28.1-blue?logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2.31.0-blue?logo=python&logoColor=white)

---

## 📦 **Arquitetura do Projeto**

```
tamarai-backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── previdenciario.py      # 🏛️ Endpoints previdenciários
│   │       └── calculadora.py         # 🧮 Calculadoras jurídicas
│   ├── core/
│   │   ├── calculators/               # 💰 Cálculos especializados
│   │   │   ├── previdenciario_calculator.py
│   │   │   ├── previdenciario_ec103_calculator.py
│   │   │   └── trabalhista_calculator.py
│   │   └── validators/                # ✅ Validações jurídicas
│   │       ├── juridico_validator.py
│   │       ├── data_validator.py
│   │       └── document_validator.py
│   ├── modules/
│   │   └── previdenciario/
│   │       ├── schemas.py             # 📋 Modelos de dados
│   │       └── service.py             # 🤖 Lógica de negócio IA
│   ├── services/
│   │   ├── ai_service.py              # 🧠 Integração OpenAI
│   │   ├── feedback_service.py        # 📊 Sistema de feedback
│   │   └── knowledge_base_enhanced.py # 📚 Base de conhecimento
│   └── main.py                        # 🚀 Aplicação principal
├── requirements.txt                   # 📦 Dependências
└── README.md                         # 📖 Documentação
```

---

## 🛠️ **Instalação e Configuração**

### **1️⃣ Clone o Repositório**
```bash
git clone https://github.com/teofilonicolau/tamarai-backend.git
cd tamarai-backend
```

### **2️⃣ Ambiente Virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configuração do Ambiente**
```bash
# Crie o arquivo .env
cp .env.example .env
```

**Arquivo `.env`:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=sqlite:///./tamarai.db
# DATABASE_URL=postgresql://user:password@localhost/tamarai

# Redis (Opcional)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256

# Environment
ENVIRONMENT=development
DEBUG=True
```

### **5️⃣ Executar a Aplicação**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 **Endpoints e Documentação**

### **📚 Documentação Interativa**
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### **🏛️ Endpoints Previdenciários**
```
POST /api/v1/previdenciario/peticao-aposentadoria-invalidez
POST /api/v1/previdenciario/peticao-revisao-vida-toda
POST /api/v1/previdenciario/peticao-aposentadoria-tempo-contribuicao
POST /api/v1/previdenciario/peticao-auxilio-doenca
POST /api/v1/previdenciario/peticao-pensao-morte
POST /api/v1/previdenciario/peticao-aposentadoria-especial
POST /api/v1/previdenciario/peticao-bpc-loas
POST /api/v1/previdenciario/peticao-aposentadoria-rural
POST /api/v1/previdenciario/peticao-salario-maternidade
POST /api/v1/previdenciario/peticao-revisao-beneficio
```

### **🧮 Endpoints de Cálculos**
```
POST /api/v1/calculadora/previdenciario
POST /api/v1/calculadora/trabalhista
GET  /api/v1/calculadora/tipos
```

### **🔍 Utilitários**
```
GET  /health                    # Status da aplicação
GET  /                         # Informações da API
```

---

## 📊 **Exemplo de Uso**

### **Gerar Petição de Aposentadoria Especial**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/previdenciario/peticao-aposentadoria-especial' \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_beneficio": "Aposentadoria Especial",
    "der": "2025-06-01",
    "motivo_recusa": "INSS alegou ausência de comprovação de exposição",
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "tempo_contribuicao_total": 25,
    "atividade_especial": true,
    "exposicao_agentes_nocivos": "Ruído acima de 85 dB",
    "valor_causa": 85000,
    "tutela_antecipada": true
  }'
```

---

## 🏆 **Diferenciais Técnicos**

### **🤖 IA Especializada**
- **Persona jurídica** treinada em Direito Previdenciário
- **Jurisprudência atualizada** de tribunais superiores
- **Argumentação técnica** de nível profissional
- **Preenchimento inteligente** de dados

### **⚖️ Qualidade Jurídica**
- **Fundamentação sólida** com leis e decretos
- **Precedentes atualizados** (STF, STJ, TNU, TRF5)
- **Estrutura processual** conforme CPC/2015
- **Tutela antecipada** quando aplicável

### **🔧 Arquitetura Modular**
- **Calculadoras especializadas** por área
- **Validadores jurídicos** integrados
- **Sistema de feedback** para melhoria contínua
- **Escalabilidade** para novas áreas do direito

---

## 🔒 **Segurança e Compliance**

### **🛡️ Medidas de Segurança**
- ✅ **Validação rigorosa** de entrada de dados
- ✅ **Sanitização** de conteúdo gerado
- ✅ **Rate limiting** para APIs
- ✅ **Logs de auditoria** para rastreabilidade

### **⚖️ Compliance Ético**
- ✅ **Disclaimers obrigatórios** em todas as petições
- ✅ **Aviso de revisão advocatícia** necessária
- ✅ **Transparência** sobre limitações da IA
- ✅ **Conformidade** com Código de Ética da OAB

---

## 🚀 **Roadmap de Desenvolvimento**

### **🎯 Próximas Funcionalidades**
- [ ] **Módulo Trabalhista** (10 tipos de petições)
- [ ] **Módulo Consumidor** (10 tipos de petições)
- [ ] **Módulo Cível** (10 tipos de petições)
- [ ] **Sistema de Templates** customizáveis
- [ ] **API de Jurisprudência** em tempo real
- [ ] **Integração com PJe** e outros sistemas

### **🔧 Melhorias Técnicas**
- [ ] **Cache inteligente** de petições similares
- [ ] **Análise de sentimento** jurídico
- [ ] **Métricas de sucesso** das petições
- [ ] **Dashboard administrativo**
- [ ] **API GraphQL** alternativa
- [ ] **Microserviços** especializados

---

## 🤝 **Contribuições**

Contribuições são muito bem-vindas! 

### **Como Contribuir:**
1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### **Áreas de Contribuição:**
- 🏛️ **Novas áreas do direito** (Trabalhista, Consumidor, Cível)
- 🤖 **Melhorias na IA** e prompts especializados
- 📊 **Calculadoras jurídicas** mais precisas
- ⚡ **Otimizações de performance**
- 📚 **Documentação** e exemplos
- 🧪 **Testes automatizados**

---

## 📈 **Estatísticas do Projeto**

![GitHub repo size](https://img.shields.io/github/repo-size/teofilonicolau/tamarai-backend)
![GitHub code size](https://img.shields.io/github/languages/code-size/teofilonicolau/tamarai-backend)
![Lines of code](https://img.shields.io/tokei/lines/github/teofilonicolau/tamarai-backend)
![GitHub last commit](https://img.shields.io/github/last-commit/teofilonicolau/tamarai-backend)

---

## 📬 **Contato e Suporte**

<div align="center">

**🏛️ TamarAI - Revolucionando a Advocacia com IA**

[![Email](https://img.shields.io/badge/Email-teofilonicolau157%40gmail.com-red?logo=gmail&logoColor=white)](mailto:teofilonicolau157@gmail.com)
[![Website](https://img.shields.io/badge/Website-www.tamarai.com-blue?logo=google-chrome&logoColor=white)](https://www.tamarai.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&logoColor=white)](https://linkedin.com/in/teofilonicolau)

**Desenvolvido com ❤️ por TamarAI**  
*Nossa meta é simplicar sua vida*

</div>

---

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**⚖️ Democratizando o acesso à justiça através da tecnologia ⚖️**

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/teofilonicolau/tamarai-backend)
[![Powered by AI](https://img.shields.io/badge/Powered%20by-AI-blue.svg)](https://openai.com)
[![Built with FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-009688.svg)](https://fastapi.tiangolo.com)

</div>
```
