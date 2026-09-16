# Bobo, o chatbot idiota

[![CI](https://github.com/condeDeveloper/chatbot-bobo/actions/workflows/ci.yml/badge.svg)](https://github.com/condeDeveloper/chatbot-bobo/actions/workflows/ci.yml)

Um chatbot de terminal em Python puro que não entende quase nada e responde com total confiança. Sem modelo de linguagem, sem API, sem dependências: só expressões regulares, um pouco de memória e muita cara de pau.

```text
Você: oi, me chamo Maria
Bobo: Prazer, Maria! Eu sou o Bobo. O nome já entrega bastante.
Você: quanto é 7 x 6?
Bobo: 42. A resposta pra tudo. Inclusive pra essa conta, por coincidência.
Você: eu estou cansada de trabalhar
Bobo: Há quanto tempo você está cansada de trabalhar?
Você: você é idiota
Bobo: Idiota é meu sobrenome. Bobo Idiota. Prazer de novo.
Você: qual é o meu nome?
Bobo: Maria! Viu? Eu presto atenção. Às vezes.
```

## Rodar

Precisa só do Python 3.10 ou mais novo.

```bash
python -m bobo               # conversa no terminal; 'sair' encerra
python -m bobo --uma "que dia é hoje"
python -m bobo --semente 42  # respostas reproduzíveis
```

Ou instale como comando: `pip install .` e depois `bobo`.

## O que ele sabe fazer (mal)

| Habilidade | Exemplos |
|------------|----------|
| Saudações e nome | "oi", "me chamo Ana", "qual é meu nome?", "tudo bem?", "tchau" |
| Matemática | "quanto é 12 * 3", "2 ^ 10", "10 / 0" (ele recusa, com dignidade) |
| Tempo | "que horas são", "que dia é hoje", "que ano é" |
| Humor | "conta uma piada", "sentido da vida", "me elogia", xingamentos, elogios, CAPS LOCK |
| Reflexões estilo ELIZA | "eu estou triste", "eu quero férias", "você é chato", "eu nunca consigo..." |
| Fallback | qualquer outra coisa: ele concorda sem entender e, depois de várias, dá dicas |

## Como é feito

```
bobo/
  texto.py          normalização: acentos, pontuação, caixa
  memoria.py        nome, humor, últimas mensagens, assuntos
  cerebro.py        passa a mensagem pelas habilidades em ordem; fallback e detecção de repetição
  habilidades/      uma classe por habilidade, cada uma devolve resposta ou None
    saudacoes.py    matematica.py    tempo.py    humor.py    eliza.py
  __main__.py       CLI com argparse
tests/              pytest
```

- A ordem das habilidades é a prioridade: saudações antes de tudo, ELIZA por último.
- O sorteio de respostas usa um `random.Random` com semente injetável, e evita repetir a resposta anterior quando há opções.
- A matemática é avaliada com `ast`, aceitando só números e operadores aritméticos, então "quanto é `__import__('os')`" não funciona.
- Relógio injetável: os testes de hora e data são determinísticos.
- Palavras-chave e padrões são comparados sem acento e sem pontuação, então "você" e "voce" dão o mesmo.

## Testes

```bash
pip install pytest
pytest
```

## Licença

MIT
