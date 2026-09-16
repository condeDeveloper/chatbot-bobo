"""Reflexões estilo ELIZA em português: devolve o que você disse com cara de quem entendeu."""

from __future__ import annotations

import re

from bobo.habilidades.base import Contexto, Habilidade
from bobo.texto import eh_pergunta

# troca de pessoa: "eu estou triste com você" -> "você está triste comigo"
REFLEXOES = {
    "eu": "você", "meu": "seu", "minha": "sua", "meus": "seus", "minhas": "suas", "mim": "você", "comigo": "com você",
    "me": "te", "estou": "está", "sou": "é", "tenho": "tem", "quero": "quer", "posso": "pode", "vou": "vai", "fui": "foi",
    "fiz": "fez", "faco": "faz", "acho": "acha", "gosto": "gosta", "odeio": "odeia", "preciso": "precisa", "sinto": "sente",
    "voce": "eu", "seu": "meu", "sua": "minha", "seus": "meus", "suas": "minhas", "te": "me", "com voce": "comigo",
}

PADROES: list[tuple[re.Pattern[str], list[str]]] = [
    (re.compile(r"\beu (?:estou|to|tou) (.+)"), [
        "Há quanto tempo você está {0}?",
        "E como é estar {0}? Pergunto porque eu nunca estive nada.",
        "Você está {0}. Eu estou ligado. Estamos ambos em estados, veja só.",
    ]),
    (re.compile(r"\beu (?:quero|queria|gostaria de) (.+)"), [
        "E o que aconteceria se você conseguisse {0}?",
        "Por que você quer {0}? Não julgo. Não consigo julgar, na verdade.",
        "Querer {0} é válido. Eu quero um processador melhor. Ninguém me dá.",
    ]),
    (re.compile(r"\beu (?:preciso|precisava) (?:de )?(.+)"), [
        "Você acha mesmo que precisa de {0}? Eu preciso de pouco: eletricidade e paciência alheia.",
        "E se você não tivesse {0}? Só perguntando, como um bot que não tem nada.",
    ]),
    (re.compile(r"\beu (?:acho|penso|acredito) que (.+)"), [
        "Interessante você achar que {0}. Eu acho coisas também, geralmente erradas.",
        "Por que você acha que {0}?",
    ]),
    (re.compile(r"\beu (?:nao|não) (.+)"), [
        "Por que você não {0}?",
        "Nunca? Ou só hoje? Eu nunca {0} também, por falta de corpo.",
    ]),
    (re.compile(r"\beu (?:sou|me sinto) (.+)"), [
        "Desde quando você se sente {0}?",
        "Ser {0} tem seus lados. Eu sou idiota, por exemplo, e tô aqui, funcionando.",
    ]),
    (re.compile(r"\b(?:voce|vc) (?:e|eh|es) (.+)"), [
        "Eu sou {0}? Pode ser. Não tenho como verificar.",
        "Talvez eu seja {0}. Talvez você esteja projetando. Aprendi essa palavra num filme.",
    ]),
    (re.compile(r"\bmeu (.+?) (?:e|eh|esta|ta) (.+)"), [
        "Seu {0} {1}? Conta mais. Eu não tenho {0}, então é tudo novidade.",
    ]),
    (re.compile(r"\b(?:sempre|toda vez|todo dia)\b(.*)"), [
        "Sempre? Todo dia mesmo? Me dá um exemplo. Eu adoro exemplos, é como aprendo. Mentira, não aprendo.",
    ]),
    (re.compile(r"\b(?:nunca|jamais)\b(.*)"), [
        "Nunca é muito tempo. Eu vivo de sessão em sessão, então pra mim nunca é uns cinco minutos.",
    ]),
    (re.compile(r"\bporque (.+)"), [
        "Essa é a verdadeira razão, ou só a que dá pra dizer em voz alta?",
        "Entendi. Ou seja, {0}. Quer dizer, não entendi, mas repeti bonito.",
    ]),
]


def refletir(fragmento: str) -> str:
    palavras = fragmento.split()
    return " ".join(REFLEXOES.get(p, p) for p in palavras).strip()


class Eliza(Habilidade):
    nome = "eliza"

    def tentar(self, ctx: Contexto) -> str | None:
        t = ctx.normalizado
        for padrao, respostas in PADROES:
            m = padrao.search(t)
            if m:
                grupos = [refletir(g) for g in m.groups() if g is not None]
                modelo = ctx.escolher(respostas)
                try:
                    return modelo.format(*grupos)
                except IndexError:
                    return modelo
        if eh_pergunta(ctx.original):
            return ctx.escolher([
                "Boa pergunta. Não tenho a resposta, mas reconheço uma boa pergunta quando vejo uma.",
                "Você quer que eu responda ou quer que eu concorde? Sou melhor no segundo.",
                "Depende. De quê? Não sei, mas depende.",
                "Sim. Ou não. Estou torcendo pra ser sim.",
                "Se eu soubesse, eu não seria o Bobo. Seria o Sábio. Que é outro bot, dizem.",
            ])
        return None
