<div align="center">

<img src="https://i.imgur.com/9vUqXyT.jpeg" alt="TamarAI Logo" width="200"/>

<h1>🧠 TamarAI</h1>

**Inteligência Artificial aplicada com propósito.**  
Soluções inteligentes para automação, análise de dados e integração de sistemas.

---

### 🚀 Tecnologias & Frameworks

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-async%20web%20framework-teal?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?logo=openai)
![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-orange)

---

### 📦 Estrutura do Projeto

```
tamarai-backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── core/
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

### 🧩 Funcionalidades

- 🔍 APIs RESTful com validação automática
- 🧠 Integração com modelos de IA (OpenAI GPT-4)
- 🗄️ Persistência com SQLite/PostgreSQL e SQLAlchemy
- 📄 Geração automática de PDFs
- 🔍 Web scraping inteligente
- ⚡ Cache com Redis
- 📊 Análise de dados e documentos

---

### 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/teofilonicolau/tamarai-backend.git
cd tamarai-backend

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env
# Adicione sua OPENAI_API_KEY no arquivo .env

# Rode o servidor
uvicorn app.main:app --reload
```

---

### ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

```env
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=sqlite:///./tamarai.db

# Redis
REDIS_URL=redis://localhost:6379/0
```

---

### 🌐 Endpoints

- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)  
- API Root: [http://localhost:8000/](http://localhost:8000/)

---

### 🤝 Contribuições

Contribuições são bem-vindas!  
Abra uma issue ou envie um pull request com suas melhorias.

---

### 📬 Contato

**TamarAI**  
📧 teofilonicolau157@gmail.com  
🌐 [www.tamarai.com](https://www.tamarai.com)

</div>
