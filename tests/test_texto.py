from bobo.texto import capitalizar, eh_pergunta, gritando, normalizar, palavras, sem_acentos


def test_remove_acentos():
    assert sem_acentos("você não é João") == "voce nao e Joao"


def test_normaliza_pontuacao_caixa_e_espacos():
    assert normalizar("  Olá,   MUNDO!!  Tudo bem?") == "ola mundo tudo bem"


def test_palavras():
    assert palavras("Eu quero... café!") == ["eu", "quero", "cafe"]


def test_pergunta_por_interrogacao_ou_palavra_inicial():
    assert eh_pergunta("Tudo bem?")
    assert eh_pergunta("quem é você")
    assert not eh_pergunta("eu estou bem")


def test_gritando():
    assert gritando("PARA COM ISSO")
    assert not gritando("OK")  # curto demais para contar como grito
    assert not gritando("Para com isso")


def test_capitalizar():
    assert capitalizar("maria") == "Maria"
    assert capitalizar("") == ""
