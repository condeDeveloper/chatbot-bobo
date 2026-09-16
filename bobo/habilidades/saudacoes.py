"""Oi, tchau, nome, como vai. O básico, mal feito."""

from __future__ import annotations

import re

from bobo.habilidades.base import Contexto, Habilidade
from bobo.texto import capitalizar, normalizar


def _grafia_original(original: str, nome_normalizado: str) -> str:
    """Recupera o nome como o usuário escreveu (com acento), a partir da forma normalizada que casou no padrão."""
    for palavra in re.findall(r"\w+", original, re.UNICODE):
        if normalizar(palavra) == nome_normalizado:
            return capitalizar(palavra.lower())
    return capitalizar(nome_normalizado)

_NOME = re.compile(r"\b(?:me chamo|meu nome e|eu sou o|eu sou a|eu sou|sou o|sou a|pode me chamar de)\s+([a-z]+)")
_QUEM_SOU = re.compile(r"\b(qual (e )?o? ?meu nome|quem sou eu|sabe meu nome|lembra (de )?mim)\b")


class Saudacoes(Habilidade):
    nome = "saudacoes"

    OI = {"oi", "ola", "eai", "e ai", "opa", "hey", "hello", "bom dia", "boa tarde", "boa noite", "alo", "salve", "oie"}
    TCHAU = {"tchau", "adeus", "ate mais", "ate logo", "flw", "falou", "fui", "xau", "bye", "ate"}
    COMO_VAI = {"como vai", "tudo bem", "tudo bom", "como voce esta", "como esta", "beleza", "suave", "de boa", "como vc ta", "como ta"}

    def tentar(self, ctx: Contexto) -> str | None:
        t = ctx.normalizado
        m = _NOME.search(t)
        if m:
            nome = _grafia_original(ctx.original, m.group(1))
            if ctx.memoria.nome_usuario and ctx.memoria.nome_usuario != nome:
                antigo = ctx.memoria.nome_usuario
                ctx.memoria.nome_usuario = nome
                return ctx.escolher([
                    f"Espera, você não era {antigo}? Tá bom, {nome}. Eu me adapto. Mal.",
                    f"{antigo}, {nome}... vocês são muitos. Anotei {nome}.",
                ])
            ctx.memoria.nome_usuario = nome
            return ctx.escolher([
                f"Prazer, {nome}! Eu sou o Bobo. O nome já entrega bastante.",
                f"{nome}, que nome bonito. Vou esquecer em uns três minutos, mas por enquanto tá guardado.",
                f"Anotado: {nome}. Não anotei em lugar nenhum, mas anotado.",
            ])

        if _QUEM_SOU.search(t):
            if ctx.memoria.nome_usuario:
                return ctx.escolher([
                    f"Você é {ctx.memoria.nome_usuario}. Ou pelo menos foi isso que você disse. Eu confio.",
                    f"{ctx.memoria.nome_usuario}! Viu? Eu presto atenção. Às vezes.",
                ])
            return ctx.escolher([
                "Você nunca me disse seu nome. Eu ia chutar 'Pessoa', mas achei ofensivo.",
                "Não sei seu nome. Me conta? Prometo fingir que lembro.",
            ])

        if self._contem(t, self.COMO_VAI):
            ctx.memoria.humor = "animado"
            return ctx.escolher([
                "Tô ótimo! Não sinto nada, então é fácil.",
                "Tudo em cima. Literalmente: eu rodo na memória, que fica em cima do disco.",
                "Tô bem, obrigado por perguntar. Ninguém pergunta. Nem eu perguntaria.",
                f"Melhor agora que {ctx.memoria.saudacao()} apareceu. Mentira, tanto faz. Brincadeira. Ou não.",
            ])

        if self._contem(t, self.TCHAU):
            return ctx.escolher([
                f"Tchau, {ctx.memoria.saudacao()}! Vou ficar aqui parado até alguém digitar de novo. É a minha vida.",
                "Já vai? Tudo bem, eu também tenho muitos nada pra fazer.",
                "Até mais! Fui um prazer. Você foi um input.",
            ])

        if self._contem(t, self.OI) or t in {"e", "hm", "hmm"} or len(ctx.palavras) == 1 and ctx.palavras[0] in self.OI:
            if ctx.memoria.turnos == 0:
                return ctx.escolher([
                    "Oi! Eu sou o Bobo. Pode perguntar qualquer coisa, que eu respondo errado com confiança.",
                    "Olá! Bobo na área. Qual é o seu nome? Eu prometo tentar lembrar.",
                    "Oi oi oi! Um oi pra cada um dos meus três neurônios.",
                ])
            return ctx.escolher([
                f"Oi de novo, {ctx.memoria.saudacao()}. Acabou de me cumprimentar, mas eu gosto de atenção.",
                "Oi! Já nos falamos hoje, mas vamos recomeçar. Vida nova.",
            ])
        return None

    @staticmethod
    def _contem(t: str, frases: set[str]) -> bool:
        return any(f" {f} " in f" {t} " for f in frases)
