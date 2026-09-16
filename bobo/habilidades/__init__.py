"""Habilidades do Bobo. Cada uma tenta responder; a primeira que conseguir, leva."""

from bobo.habilidades.base import Contexto, Habilidade
from bobo.habilidades.eliza import Eliza
from bobo.habilidades.humor import Humor
from bobo.habilidades.matematica import Matematica
from bobo.habilidades.saudacoes import Saudacoes
from bobo.habilidades.tempo import Tempo

__all__ = ["Contexto", "Habilidade", "Saudacoes", "Matematica", "Tempo", "Humor", "Eliza"]
