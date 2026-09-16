"""Normalização de texto: sem acentos, sem pontuação, minúsculo, espaços únicos."""

from __future__ import annotations

import re
import unicodedata

_PONTUACAO = re.compile(r"[^\w\s]", re.UNICODE)
_ESPACOS = re.compile(r"\s+")


def sem_acentos(texto: str) -> str:
    """Remove marcas diacríticas: 'você não é' -> 'voce nao e'."""
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def normalizar(texto: str) -> str:
    """Forma canônica usada para casar padrões."""
    t = sem_acentos(texto).lower()
    t = _PONTUACAO.sub(" ", t)
    return _ESPACOS.sub(" ", t).strip()


def palavras(texto: str) -> list[str]:
    return normalizar(texto).split()


def eh_pergunta(texto: str) -> bool:
    t = texto.strip()
    if t.endswith("?"):
        return True
    primeira = palavras(t)[:1]
    return primeira[0] in {"quem", "que", "qual", "quando", "onde", "como", "por", "porque", "cade", "quanto", "quantos", "quantas"} if primeira else False


def gritando(texto: str) -> bool:
    letras = [c for c in texto if c.isalpha()]
    return len(letras) >= 4 and all(c.isupper() for c in letras)


def capitalizar(texto: str) -> str:
    return texto[:1].upper() + texto[1:] if texto else texto
