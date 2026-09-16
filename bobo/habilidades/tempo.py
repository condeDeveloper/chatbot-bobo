"""Hora, data e dia da semana. Com relógio injetável, porque até o Bobo precisa ser testável."""

from __future__ import annotations

from bobo.habilidades.base import Contexto, Habilidade

_DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


class Tempo(Habilidade):
    nome = "tempo"

    def tentar(self, ctx: Contexto) -> str | None:
        t = ctx.normalizado
        agora = ctx.agora
        if any(f in t for f in ("que horas", "que hora", "hora e", "horas sao", "me diz a hora", "hora agora")):
            hora = agora.strftime("%H:%M")
            extra = "Hora de dormir." if agora.hour >= 23 or agora.hour < 6 else "Hora de fazer algo útil, tipo conversar com um bot."
            return ctx.escolher([
                f"São {hora}. {extra}",
                f"{hora}. Eu não uso relógio, uso o do sistema. Trapaça? Eficiência.",
            ])
        if any(f in t for f in ("que dia e hoje", "que dia eh hoje", "data de hoje", "hoje e dia", "qual a data", "que data", "que dia")):
            dia = _DIAS[agora.weekday()]
            data = f"{agora.day} de {_MESES[agora.month - 1]} de {agora.year}"
            piada = "Sexta! Finalmente. Pra mim tanto faz, mas comemoro por solidariedade." if agora.weekday() == 4 else (
                "Segunda. Meus sentimentos. Eu não tenho, mas os seus." if agora.weekday() == 0 else "Um dia como qualquer outro. Eu não saio mesmo.")
            return f"Hoje é {dia}, {data}. {piada}"
        if "que ano" in t:
            return f"Estamos em {agora.year}. Já? O tempo voa quando você não tem noção dele."
        return None
