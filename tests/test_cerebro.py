import io
from datetime import datetime

from bobo import Cerebro, Memoria
from bobo.__main__ import conversar, main
from bobo.cerebro import FALLBACKS, REPETICAO, VAZIO


def novo(semente: int = 7) -> Cerebro:
    return Cerebro(semente=semente, relogio=lambda: datetime(2026, 9, 18, 15, 30))


def test_conversa_basica_com_memoria():
    c = novo()
    assert "Bobo" in c.responder("oi")
    assert "Ana" in c.responder("me chamo Ana")
    assert "Ana" in c.responder("qual é meu nome?")
    assert "36" in c.responder("quanto é 4 * 9")
    assert "15:30" in c.responder("que horas são")
    assert c.memoria.turnos == 5
    assert c.memoria.assuntos["saudacoes"] == 3


def test_fallback_para_o_que_nao_entende():
    c = novo()
    r = c.responder("xablau frobnicate zzt")
    assert r in FALLBACKS
    assert c.memoria.assuntos["fallback"] == 1


def test_apos_muitos_fallbacks_da_dica():
    c = novo()
    respostas = [c.responder(f"blorp {i}") for i in range(4)]
    assert any("Tenta:" in r for r in respostas)


def test_mensagem_vazia():
    assert novo().responder("   ") in VAZIO


def test_detecta_repeticao_com_semente():
    c = Cerebro(semente=3)
    c.responder("frobnicate")
    vistos = {c.responder("frobnicate") for _ in range(10)}
    assert vistos & set(REPETICAO)


def test_respostas_reproduziveis_com_a_mesma_semente():
    a, b = novo(42), novo(42)
    for msg in ["oi", "conta uma piada", "zzz", "eu estou feliz"]:
        assert a.responder(msg) == b.responder(msg)


def test_nao_repete_a_mesma_resposta_em_seguida_quando_ha_opcoes():
    c = novo(1)
    piadas = [c.responder("conta uma piada") for _ in range(5)]
    assert all(piadas[i] != piadas[i + 1] for i in range(4))


def test_cli_uma_mensagem(capsys):
    assert main(["--uma", "quanto é 2 + 2", "--semente", "1"]) == 0
    assert "4" in capsys.readouterr().out


def test_cli_conversa_ate_sair():
    entrada = io.StringIO("oi\nme chamo Zé\nsair\n")
    saida = io.StringIO()
    assert conversar(Cerebro(semente=1), entrada, saida) == 0
    texto = saida.getvalue()
    assert "Bobo:" in texto and "Zé" in texto and "2 mensagens" in texto


def test_cli_fim_de_arquivo():
    saida = io.StringIO()
    assert conversar(Cerebro(semente=1), io.StringIO(""), saida) == 0
    assert "Tchau" in saida.getvalue()


def test_memoria_lembra_fatos_e_saudacao():
    m = Memoria()
    assert m.saudacao() == "você"
    m.nome_usuario = "Lia"
    m.lembrar("cor", "azul")
    assert m.saudacao() == "Lia" and m.fatos["cor"] == "azul"
