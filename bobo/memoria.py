"""Memória de curto prazo da conversa: o pouco que o Bobo consegue lembrar."""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field


@dataclass
class Memoria:
    nome_usuario: str | None = None
    humor: str = "neutro"
    turnos: int = 0
    ultimas_mensagens: deque[str] = field(default_factory=lambda: deque(maxlen=6))
    ultimas_respostas: deque[str] = field(default_factory=lambda: deque(maxlen=6))
    assuntos: Counter[str] = field(default_factory=Counter)
    fatos: dict[str, str] = field(default_factory=dict)

    def registrar(self, mensagem: str, resposta: str) -> None:
        self.turnos += 1
        self.ultimas_mensagens.append(mensagem)
        self.ultimas_respostas.append(resposta)

    def lembrar(self, chave: str, valor: str) -> None:
        self.fatos[chave] = valor

    def repetiu(self, mensagem: str) -> bool:
        """Verdadeiro se a mensagem é igual à anterior (o Bobo percebe, às vezes)."""
        return len(self.ultimas_mensagens) > 0 and self.ultimas_mensagens[-1] == mensagem

    def ja_respondeu(self, resposta: str) -> bool:
        return resposta in self.ultimas_respostas

    def saudacao(self) -> str:
        return f"{self.nome_usuario}" if self.nome_usuario else "você"
