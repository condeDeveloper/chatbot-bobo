"""O Bobo faz contas. Certas, o que estraga um pouco a piada. Ele compensa comentando."""

from __future__ import annotations

import ast
import operator
import re

from bobo.habilidades.base import Contexto, Habilidade

_EXPRESSAO = re.compile(r"(-?\d+(?:[.,]\d+)?(?:\s*[-+*/x×÷^%]\s*-?\d+(?:[.,]\d+)?)+)")
_QUANTO_E = re.compile(r"\b(quanto e|quanto da|calcula|calcule|resolve|some|soma|multiplica|divide)\b")

_OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def avaliar(expressao: str) -> float:
    """Avalia aritmética simples com segurança (só números e + - * / % **)."""
    limpa = expressao.replace(",", ".").replace("x", "*").replace("×", "*").replace("÷", "/").replace("^", "**")
    arvore = ast.parse(limpa, mode="eval")
    return _avaliar_no(arvore.body)


def _avaliar_no(no: ast.AST) -> float:
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return float(no.value)
    if isinstance(no, ast.BinOp) and type(no.op) in _OPERADORES:
        esq, dir_ = _avaliar_no(no.left), _avaliar_no(no.right)
        if isinstance(no.op, ast.Pow) and abs(dir_) > 64:
            raise ValueError("expoente grande demais")
        if isinstance(no.op, (ast.Div, ast.Mod)) and dir_ == 0:
            raise ZeroDivisionError
        return _OPERADORES[type(no.op)](esq, dir_)
    if isinstance(no, ast.UnaryOp) and type(no.op) in _OPERADORES:
        return _OPERADORES[type(no.op)](_avaliar_no(no.operand))
    raise ValueError("expressão não suportada")


def formatar(n: float) -> str:
    if n == int(n) and abs(n) < 1e15:
        return str(int(n))
    return f"{n:.4f}".rstrip("0").rstrip(".")


class Matematica(Habilidade):
    nome = "matematica"

    def tentar(self, ctx: Contexto) -> str | None:
        m = _EXPRESSAO.search(ctx.original.lower())
        if not m and not _QUANTO_E.search(ctx.normalizado):
            return None
        if not m:
            return ctx.escolher([
                "Conta eu faço, mas você precisa me dar os números. Tipo '2 + 2'. Eu sei, é pedir muito.",
                "Manda a conta com número e sinal que eu resolvo. Ou tento. Provavelmente resolvo.",
            ])
        try:
            resultado = avaliar(m.group(1))
        except ZeroDivisionError:
            return "Dividir por zero? Não. Eu sou idiota, não maluco."
        except (ValueError, SyntaxError, OverflowError):
            return "Essa conta quebrou meu cérebro, e ele já era pequeno."

        r = formatar(resultado)
        comentarios = [
            f"{m.group(1).strip()} dá {r}. Acertei sem querer.",
            f"É {r}. Contei nos dedos. Tenho dedos virtuais infinitos, é uma vantagem.",
            f"{r}. Se estiver errado, a culpa é da matemática, não minha.",
            f"Deu {r}. Não me pergunte como, foi tipo um sentimento.",
        ]
        if resultado == 42:
            comentarios = ["42. A resposta pra tudo. Inclusive pra essa conta, por coincidência."]
        elif resultado < 0:
            comentarios.append(f"{r}. Negativo. Igual meu saldo de auto-estima.")
        return ctx.escolher(comentarios)
