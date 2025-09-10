# app/api/routes/__init__.py
"""
Módulo de rotas da API TamarUSE
"""

# Importar todos os routers disponíveis
try:
    from . import calculadoras
except ImportError:
    print("⚠️ Aviso: calculadoras.py não encontrado")
    calculadoras = None

try:
    from . import peticoes
except ImportError:
    print("⚠️ Aviso: peticoes.py não encontrado")
    peticoes = None

try:
    from . import consultas
except ImportError:
    print("⚠️ Aviso: consultas.py não encontrado")
    consultas = None

try:
    from . import calculadora
except ImportError:
    print("⚠️ Aviso: calculadora.py não encontrado")
    calculadora = None

try:
    from . import analytics
except ImportError:
    print("⚠️ Aviso: analytics.py não encontrado")
    analytics = None

try:
    from . import trabalhista
except ImportError:
    print("⚠️ Aviso: trabalhista.py não encontrado")
    trabalhista = None

try:
    from . import consumidor
except ImportError:
    print("⚠️ Aviso: consumidor.py não encontrado")
    consumidor = None

try:
    from . import previdenciario
except ImportError:
    print("⚠️ Aviso: previdenciario.py não encontrado")
    previdenciario = None

try:
    from . import civil
except ImportError:
    print("⚠️ Aviso: civil.py não encontrado")
    civil = None

try:
    from . import processual_civil
except ImportError:
    print("⚠️ Aviso: processual_civil.py não encontrado")
    processual_civil = None

# Lista de routers disponíveis
__all__ = [
    "calculadoras",
    "peticoes", 
    "consultas",
    "calculadora",
    "analytics",
    "trabalhista",
    "consumidor",
    "previdenciario",
    "civil",
    "processual_civil"
]