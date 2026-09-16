"""Bobo no terminal: python -m bobo"""

from __future__ import annotations

import argparse
import sys

from bobo import __version__
from bobo.cerebro import Cerebro

BANNER = r"""
  ____        _
 |  _ \      | |
 | |_) | ___ | |__   ___
 |  _ < / _ \| '_ \ / _ \
 | |_) | (_) | |_) | (_) |
 |____/ \___/|_.__/ \___/   v{versao}
 o chatbot idiota. digite 'sair' quando cansar.
"""


def conversar(cerebro: Cerebro, entrada=None, saida=None) -> int:
    entrada = entrada or sys.stdin
    saida = saida or sys.stdout
    print(BANNER.format(versao=__version__), file=saida)
    print("Bobo: Oi! Eu sou o Bobo. Fala qualquer coisa. Eu respondo. Se vai fazer sentido, é outra história.", file=saida)
    while True:
        try:
            print("Você: ", end="", file=saida, flush=True)
            linha = entrada.readline()
        except (KeyboardInterrupt, EOFError):
            print("\nBobo: Saiu na marra. Respeito.", file=saida)
            return 0
        if not linha:
            print("\nBobo: Acabou o texto? Tá bom. Tchau.", file=saida)
            return 0
        mensagem = linha.rstrip("\n")
        if mensagem.strip().lower() in {"sair", "exit", "quit", "tchau bobo", "xau bobo"}:
            print(f"Bobo: Tchau, {cerebro.memoria.saudacao()}! Foram {cerebro.memoria.turnos} mensagens. Nenhuma fez sentido. Perfeito.", file=saida)
            return 0
        print(f"Bobo: {cerebro.responder(mensagem)}", file=saida)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bobo", description="Chatbot idiota de terminal.")
    parser.add_argument("--semente", type=int, default=None, help="semente do sorteio, para respostas reproduzíveis")
    parser.add_argument("--uma", metavar="MENSAGEM", help="responde uma mensagem e sai")
    args = parser.parse_args(argv)
    cerebro = Cerebro(semente=args.semente)
    if args.uma is not None:
        print(cerebro.responder(args.uma))
        return 0
    return conversar(cerebro)


if __name__ == "__main__":
    raise SystemExit(main())
