# 🆕 CRIAR: app/services/planilha_generator.py
class PlanilhaGenerator:
    def gerar_por_beneficio(self, tipo_beneficio, dados):
        templates = {
            "aposentadoria_tempo": self._template_tempo_contribuicao,
            "revisao_vida_toda": self._template_vida_toda,
            "auxilio_doenca": self._template_auxilio_doenca
        }
        return templates[tipo_beneficio](dados)# 🆕 CRIAR: app/services/planilha_generator.py
class PlanilhaGenerator:
    def gerar_por_beneficio(self, tipo_beneficio, dados):
        templates = {
            "aposentadoria_tempo": self._template_tempo_contribuicao,
            "revisao_vida_toda": self._template_vida_toda,
            "auxilio_doenca": self._template_auxilio_doenca
        }
        return templates[tipo_beneficio](dados)# 🆕 CRIAR: app/services/planilha_generator.py
class PlanilhaGenerator:
    def gerar_por_beneficio(self, tipo_beneficio, dados):
        templates = {
            "aposentadoria_tempo": self._template_tempo_contribuicao,
            "revisao_vida_toda": self._template_vida_toda,
            "auxilio_doenca": self._template_auxilio_doenca
        }
        return templates[tipo_beneficio](dados)