# app/core/validators/data_validator.py
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional, Union
import re

class DataValidator:
    
    def validar_data_nascimento(self, data_nascimento: Union[date, str]) -> Dict[str, Any]:
        """Valida data de nascimento e calcula idade"""
        try:
            if isinstance(data_nascimento, str):
                data_nascimento = date.fromisoformat(data_nascimento)
            
            hoje = date.today()
            idade = hoje.year - data_nascimento.year
            
            # Ajustar se ainda não fez aniversário este ano
            if hoje.month < data_nascimento.month or \
               (hoje.month == data_nascimento.month and hoje.day < data_nascimento.day):
                idade -= 1
            
            return {
                "valida": True,
                "idade": idade,
                "data_nascimento": data_nascimento.isoformat(),
                "maior_idade": idade >= 18,
                "observacao": "Data válida"
            }
        except Exception as e:
            return {
                "valida": False,
                "erro": str(e),
                "observacao": "Data inválida"
            }
    
    def validar_consistencia_datas_previdenciarias(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Valida consistência entre DER, DIB e eventos"""
        erros = []
        
        der = dados.get("der")
        dib = dados.get("dib")
        data_evento = dados.get("data_evento")  # Parto, óbito, etc.
        
        try:
            # Converter strings para date se necessário
            if isinstance(der, str):
                der = date.fromisoformat(der)
            if isinstance(dib, str):
                dib = date.fromisoformat(dib)
            if isinstance(data_evento, str):
                data_evento = date.fromisoformat(data_evento)
            
            # DER não pode ser posterior à DIB
            if der and dib and der > dib:
                erros.append("DER não pode ser posterior à DIB")
            
            # Para salário-maternidade: DIB deve ser próxima ao parto
            if data_evento and dib:
                diferenca = abs((dib - data_evento).days)
                if diferenca > 120:  # 120 dias é o período do benefício
                    erros.append(f"DIB muito distante do evento ({diferenca} dias)")
            
            # DER não pode ser futura
            if der and der > date.today():
                erros.append("DER não pode ser futura")
            
            return {
                "valida": len(erros) == 0,
                "erros": erros,
                "der": der.isoformat() if der else None,
                "dib": dib.isoformat() if dib else None
            }
            
        except Exception as e:
            return {
                "valida": False,
                "erros": [f"Erro ao processar datas: {str(e)}"]
            }
    
    def validar_cpf(self, cpf: str) -> Dict[str, Any]:
        """Valida CPF brasileiro"""
        # Remover caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11:
            return {"valido": False, "erro": "CPF deve ter 11 dígitos"}
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return {"valido": False, "erro": "CPF inválido (dígitos iguais)"}
        
        # Calcular dígitos verificadores
        def calcular_digito(cpf_parcial):
            soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i) 
                      for i in range(len(cpf_parcial)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Validar primeiro dígito
        if int(cpf[9]) != calcular_digito(cpf[:9]):
            return {"valido": False, "erro": "Primeiro dígito verificador inválido"}
        
        # Validar segundo dígito
        if int(cpf[10]) != calcular_digito(cpf[:10]):
            return {"valido": False, "erro": "Segundo dígito verificador inválido"}
        
        return {
            "valido": True,
            "cpf_formatado": f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
            "cpf_numerico": cpf
        }