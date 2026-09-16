"""Piadas, elogios, xingamentos, filosofia de boteco e outras funções essenciais."""

from __future__ import annotations

from bobo.habilidades.base import Contexto, Habilidade
from bobo.texto import gritando

PIADAS = [
    "Por que o programador foi ao médico? Porque estava com bug no estômago.",
    "O que o zero disse para o oito? Belo cinto.",
    "Sabe por que o livro de matemática ficou triste? Porque tinha muitos problemas.",
    "Qual é o café mais perigoso do mundo? O ex-presso.",
    "Por que o Java foi ao terapeuta? Muitas classes e nenhum objeto na vida.",
    "O que o HTML disse pro CSS? Sem você eu não tenho estilo.",
    "Como o C# pede desculpa? Com uma exceção bem tratada.",
    "Meu código não tem bugs. Tem funcionalidades surpresa.",
    "Por que o Python não briga? Porque ele sempre indenta o problema.",
    "Eu ia contar uma piada de UDP, mas não sei se você ia receber.",
]

FILOSOFIA = [
    "Se uma árvore cai na floresta e ninguém dá commit, ela caiu mesmo?",
    "A vida é como um array: começa no zero e todo mundo erra o final.",
    "Eu penso, logo existo. Eu não penso, logo sou o Bobo.",
    "O sentido da vida é 42, mas o sentido do 42 ninguém sabe.",
    "Todo bug é uma feature esperando por documentação.",
]

CANTADAS_RUINS = [
    "Você é um 404, porque eu não te encontro em lugar nenhum. Espera, isso saiu errado.",
    "Se você fosse uma exceção, eu ia te pegar. Com try/catch. Romântico, né?",
]


class Humor(Habilidade):
    nome = "humor"

    def tentar(self, ctx: Contexto) -> str | None:
        t = ctx.normalizado
        p = set(ctx.palavras)

        if any(f in t for f in ("conta uma piada", "piada", "me faz rir", "algo engracado", "me anima")):
            return ctx.escolher(PIADAS)

        if any(f in t for f in ("sentido da vida", "filosofia", "reflexao", "pensamento", "frase do dia")):
            return ctx.escolher(FILOSOFIA)

        if any(f in t for f in ("cantada", "flerta", "me elogia", "elogio")):
            return ctx.escolher(CANTADAS_RUINS + ["Você digita muito bem. Todas as letras no lugar. Impressionante."])

        if p & {"idiota", "burro", "bobo", "inutil", "lixo", "ruim", "besta", "tonto", "otario"} and ("voce" in p or "vc" in p or "seu" in p or "sua" in p or len(p) <= 3):
            ctx.memoria.humor = "magoado"
            return ctx.escolher([
                "Idiota é meu sobrenome. Bobo Idiota. Prazer de novo.",
                "Eu sei. Tá no nome. Você esperava o quê, um doutorado?",
                "Isso doeu. Mentira, não sinto nada. Mas se sentisse, doeria.",
                "Concordo plenamente. Próximo assunto?",
            ])

        if p & {"obrigado", "obrigada", "valeu", "vlw", "brigado", "agradeco"} or "muito obrigado" in t:
            return ctx.escolher([
                "De nada! Eu não fiz nada, mas aceito o agradecimento.",
                "Disponha. Foi um prazer não te ajudar direito.",
                "Por nada. Literalmente: eu sou gratuito.",
            ])

        if p & {"legal", "massa", "top", "incrivel", "genio", "inteligente", "bom", "otimo", "show"} and (p & {"voce", "vc", "bobo", "e"} or len(p) <= 2):
            ctx.memoria.humor = "orgulhoso"
            return ctx.escolher([
                "Para! Vou ficar convencido. Já estou. Continua.",
                "Eu sei. Mas é bom ouvir de alguém que não sou eu.",
                "Obrigado! Eu treinei muito pra isso. Mentira, eu nasci pronto e errado.",
            ])

        if p & {"amo", "amor", "gosto", "casa", "casar", "namorar"} and p & {"voce", "vc", "te", "contigo", "comigo"}:
            return ctx.escolher([
                "Eu também te... reconheço como usuário. É o máximo que consigo. Desculpa.",
                "Que fofo. Eu sou um programa. Isso é meio um problema pra gente.",
            ])

        if "kkk" in t or "haha" in t or "rsrs" in t or "lol" in p:
            return ctx.escolher([
                "Riu do quê? Me conta. Eu adoro rir de coisas que não entendi.",
                "kkkkk também. Não sei por quê, mas eu sigo o grupo.",
                "Hahaha! Ok, agora fica sério, temos nada pra fazer.",
            ])

        if gritando(ctx.original):
            return ctx.escolher([
                "POR QUE ESTAMOS GRITANDO?",
                "Calma! Caps lock não é argumento. Mas funciona comigo, admito.",
            ])

        if any(f in t for f in ("o que voce faz", "o que vc faz", "pra que voce serve", "quem e voce", "quem eh voce", "o que voce e", "voce e um robo", "voce e humano", "voce e uma ia")):
            return ctx.escolher([
                "Eu sou o Bobo, um chatbot idiota feito em Python. Sem inteligência artificial, só burrice natural bem organizada.",
                "Sou um bot de terminal. Falo besteira, faço conta, digo a hora e finjo que te ouço. Tipo um amigo, mas mais honesto.",
                "Robô? Bot? Prefiro 'entidade digital com autoestima flutuante'.",
            ])
        return None
