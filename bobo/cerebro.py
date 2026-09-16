"""O Cérebro do Bobo: coordena as habilidades e decide o que sai pela boca."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Callable

from bobo.habilidades import Contexto, Eliza, Habilidade, Humor, Matematica, Saudacoes, Tempo
from bobo.memoria import Memoria
from bobo.texto import normalizar, palavras

FALLBACKS = [
    "Não entendi, mas concordo.",
    "Interessante. Não sei o que é, mas interessante.",
    "Hm. Pode repetir de um jeito que um bot idiota entenda?",
    "Isso me lembra uma coisa. Esqueci o quê. Continua.",
    "Anotado. Em nenhum lugar. Mas anotado.",
    "Você disse isso pra mim ou pra vida? Porque a vida não responde. Eu respondo. Errado, mas respondo.",
    "Entendi tudo. Menos as palavras.",
    "Certo. E como isso faz você se sentir? Sempre quis dizer essa frase.",
]

REPETICAO = [
    "Você já disse isso. Eu lembro, tenho memória de seis mensagens. Aproveita.",
    "De novo? Tá bom, eu respondo a mesma coisa com outras palavras: não entendi.",
    "Repetir não me ajuda a entender. Nada ajuda, na verdade.",
]

VAZIO = [
    "Você mandou o vazio. Eu respeito. O vazio é meu estado natural.",
    "Um enter sem nada. Poético. Ou um dedo escorregou.",
    "...",
]


class Cerebro:
    """Passa a mensagem por cada habilidade, em ordem, e cai no fallback se ninguém responder."""

    def __init__(
        self,
        memoria: Memoria | None = None,
        habilidades: list[Habilidade] | None = None,
        semente: int | None = None,
        relogio: Callable[[], datetime] | None = None,
    ) -> None:
        self.memoria = memoria or Memoria()
        self.habilidades: list[Habilidade] = habilidades or [Saudacoes(), Matematica(), Tempo(), Humor(), Eliza()]
        self.rng = random.Random(semente)
        self.relogio = relogio or datetime.now

    def responder(self, mensagem: str) -> str:
        original = mensagem.strip()
        if not original:
            resposta = self.rng.choice(VAZIO)
            self.memoria.registrar(original, resposta)
            return resposta

        ctx = Contexto(original=original, normalizado=normalizar(original), palavras=palavras(original), memoria=self.memoria, rng=self.rng, agora=self.relogio())

        if self.memoria.repetiu(original) and self.rng.random() < 0.7:
            resposta = ctx.escolher(REPETICAO)
        else:
            resposta = self._perguntar_habilidades(ctx) or self._fallback(ctx)

        self.memoria.registrar(original, resposta)
        return resposta

    def _perguntar_habilidades(self, ctx: Contexto) -> str | None:
        for habilidade in self.habilidades:
            resposta = habilidade.tentar(ctx)
            if resposta:
                self.memoria.assuntos[habilidade.nome] += 1
                return resposta
        return None

    def _fallback(self, ctx: Contexto) -> str:
        self.memoria.assuntos["fallback"] += 1
        # depois de muito fallback, o Bobo assume a limitação
        if self.memoria.assuntos["fallback"] % 4 == 0:
            return "Tá difícil hoje, né? Tenta: me conta uma piada, que horas são, quanto é 7 x 6, ou me diz como você está."
        return ctx.escolher(FALLBACKS)
