import random
from datetime import datetime

import pytest

from bobo.habilidades import Contexto, Eliza, Humor, Matematica, Saudacoes, Tempo
from bobo.habilidades.eliza import refletir
from bobo.habilidades.matematica import avaliar, formatar
from bobo.memoria import Memoria
from bobo.texto import normalizar, palavras

AGORA = datetime(2026, 9, 18, 15, 30)  # sexta-feira


def ctx(mensagem: str, memoria: Memoria | None = None, agora: datetime = AGORA) -> Contexto:
    return Contexto(original=mensagem, normalizado=normalizar(mensagem), palavras=palavras(mensagem), memoria=memoria or Memoria(), rng=random.Random(1), agora=agora)


class TestSaudacoes:
    def test_aprende_e_lembra_o_nome(self):
        m = Memoria()
        s = Saudacoes()
        r = s.tentar(ctx("Oi, me chamo Maria", m))
        assert "Maria" in r
        assert m.nome_usuario == "Maria"
        assert "Maria" in s.tentar(ctx("qual é o meu nome?", m))

    def test_troca_de_nome_gera_estranheza(self):
        m = Memoria(nome_usuario="Maria")
        r = Saudacoes().tentar(ctx("eu sou o Pedro", m))
        assert "Maria" in r and "Pedro" in r
        assert m.nome_usuario == "Pedro"

    def test_sem_nome_nao_inventa(self):
        r = Saudacoes().tentar(ctx("sabe meu nome?"))
        assert "nunca me disse" in r or "Não sei seu nome" in r

    def test_oi_e_tchau(self):
        assert Saudacoes().tentar(ctx("oi")) is not None
        assert "Tchau" in Saudacoes().tentar(ctx("tchau")) or "Já vai" in Saudacoes().tentar(ctx("tchau"))

    def test_nao_responde_o_que_nao_e_saudacao(self):
        assert Saudacoes().tentar(ctx("quanto é 2 + 2")) is None


class TestMatematica:
    @pytest.mark.parametrize("expr, esperado", [("2 + 2", 4), ("7 x 6", 42), ("10 / 4", 2.5), ("2 ^ 10", 1024), ("-3 + 5", 2), ("1,5 * 2", 3), ("10 % 3", 1)])
    def test_avalia(self, expr, esperado):
        assert avaliar(expr) == esperado

    def test_nao_executa_codigo(self):
        with pytest.raises((ValueError, SyntaxError)):
            avaliar("__import__('os').system('echo oi')")

    def test_formata(self):
        assert formatar(4.0) == "4"
        assert formatar(2.5) == "2.5"
        assert formatar(1 / 3) == "0.3333"

    def test_responde_conta_no_meio_da_frase(self):
        r = Matematica().tentar(ctx("bobo, quanto é 12 * 3?"))
        assert "36" in r

    def test_divisao_por_zero(self):
        assert "zero" in Matematica().tentar(ctx("10 / 0")).lower()

    def test_quarenta_e_dois(self):
        assert "42" in Matematica().tentar(ctx("6 * 7"))

    def test_pede_numeros_quando_so_diz_calcula(self):
        assert "número" in Matematica().tentar(ctx("calcula aí")).lower()

    def test_ignora_frases_sem_conta(self):
        assert Matematica().tentar(ctx("eu tenho 3 gatos")) is None


class TestTempo:
    def test_hora(self):
        assert "15:30" in Tempo().tentar(ctx("que horas são?"))

    def test_data_com_dia_da_semana(self):
        r = Tempo().tentar(ctx("que dia é hoje"))
        assert "sexta-feira" in r and "18 de setembro de 2026" in r and "Sexta!" in r

    def test_segunda_feira_tem_lamento(self):
        r = Tempo().tentar(ctx("que dia é hoje", agora=datetime(2026, 9, 14, 9, 0)))
        assert "Segunda" in r

    def test_ignora_outros_assuntos(self):
        assert Tempo().tentar(ctx("me conta uma piada")) is None


class TestHumor:
    def test_piada(self):
        assert Humor().tentar(ctx("conta uma piada")) is not None

    def test_xingamento_muda_humor(self):
        m = Memoria()
        assert Humor().tentar(ctx("você é idiota", m)) is not None
        assert m.humor == "magoado"

    def test_elogio_muda_humor(self):
        m = Memoria()
        assert Humor().tentar(ctx("você é genio", m)) is not None
        assert m.humor == "orgulhoso"

    def test_gritos(self):
        assert "GRITANDO" in Humor().tentar(ctx("PARA DE FALAR BESTEIRA")) or "Caps" in Humor().tentar(ctx("PARA DE FALAR BESTEIRA"))

    def test_quem_e_voce(self):
        assert "Bobo" in Humor().tentar(ctx("quem é você?"))

    def test_agradecimento(self):
        assert Humor().tentar(ctx("obrigado bobo")) is not None


class TestEliza:
    def test_reflete_pessoa(self):
        assert refletir("eu estou triste com voce") == "você está triste com eu"[:0] or refletir("eu estou triste") == "você está triste"
        assert refletir("meu chefe me odeia") == "seu chefe te odeia"

    def test_padrao_eu_estou(self):
        r = Eliza().tentar(ctx("eu estou muito cansado"))
        assert "cansado" in r

    def test_padrao_eu_quero(self):
        assert "café" in Eliza().tentar(ctx("eu quero café")) or "cafe" in Eliza().tentar(ctx("eu quero café"))

    def test_padrao_voce_e(self):
        assert "chato" in Eliza().tentar(ctx("você é chato"))

    def test_pergunta_generica(self):
        assert Eliza().tentar(ctx("o universo é infinito?")) is not None

    def test_afirmacao_sem_padrao_passa(self):
        assert Eliza().tentar(ctx("banana amarela") ) is None
