# app/services/knowledge_base.py
class KnowledgeBase:
    
    def __init__(self):
        self.doutrinadores = {
            'trabalhista': [
                'Mauricio Godinho Delgado',
                'Alice Monteiro de Barros', 
                'Vólia Bomfim Cassar',
                'Sergio Pinto Martins'
            ],
            'previdenciario': [
                'Miguel Horvath Júnior',
                'Wladimir Novaes Martinez',
                'Daniel Machado da Rocha'
            ]
        }
        
        self.sumulas_tst = {
            '6': 'EQUIPARAÇÃO SALARIAL. ART. 461 DA CLT',
            '338': 'JORNADA DE TRABALHO. REGISTRO DE PONTO',
            '428': 'SOBREAVISO. APLICAÇÃO ANALÓGICA'
        }
    
    async def get_fundamento_doutrinario(self, area: str, tema: str) -> str:
        """Retorna fundamento doutrinário específico"""
        if area == 'trabalhista' and tema == 'vinculo':
            return """
            Segundo Mauricio Godinho Delgado, os elementos caracterizadores da relação 
            de emprego são: pessoalidade, não eventualidade, onerosidade e subordinação.
            A configuração destes elementos, ainda que de forma tênue, caracteriza o 
            vínculo empregatício, conforme arts. 2º e 3º da CLT.
            """