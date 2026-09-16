"""Contrato das habilidades."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from bobo.memoria import Memoria


@dataclass
class Contexto:
    """Tudo que uma habilidade pode precisar para responder."""

    original: str
    normalizado: str
    palavras: list[str]
    memoria: Memoria
    rng: random.Random
    agora: datetime

    def escolher(self, opcoes: list[str]) -> str:
        """Sorteia evitando repetir a última resposta, quando dá."""
        candidatas = [o for o in opcoes if not self.memoria.ja_respondeu(o)] or opcoes
        return self.rng.choice(candidatas)


class Habilidade(ABC):
    """Uma habilidade devolve uma resposta ou None se não souber lidar com a mensagem."""

    nome: str = "habilidade"

    @abstractmethod
    def tentar(self, ctx: Contexto) -> str | None: ...
