# Segunda Máquina de Turing: Reconhece "aa seguido de bb"

## Descrição
Esta MT reconhece palavras da forma "a^n b^n" onde n ≥ 1, ou seja, uma sequência de 'a's seguida pela mesma quantidade de 'b's.

## Estados
- q1: Estado inicial
- q11: Lendo sequência de a's
- q111: Encontrou primeiro b, voltando para marcar a
- q1111: Marcando a's e b's correspondentes
- qf: Estado final de aceitação

## Alfabeto
- a1: símbolo 'a'
- a11: símbolo 'b' 
- a111: símbolo 'a' marcado (X)
- a1111: símbolo 'b' marcado (Y)
- b: símbolo branco
- s: símbolo de início da fita

## Tabela de Transições

| Estado Atual | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado |
|--------------|--------------|-----------------|-----------|----------------|
| q1           | s            | s               | R         | q1             |
| q1           | a1           | a111            | R         | q11            |
| q11          | a1           | a1              | R         | q11            |
| q11          | a11          | a1111           | L         | q111           |
| q111         | a1           | a1              | L         | q111           |
| q111         | a111         | a111            | L         | q111           |
| q111         | s            | s               | R         | q1111          |
| q1111        | a111         | a111            | R         | q1111          |
| q1111        | a1           | a111            | R         | q11            |
| q1111        | a1111        | a1111           | R         | q1111          |
| q1111        | b            | b               | R         | qf             |

## Codificação Unária

```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111a111a111Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf
```

## Palavras de Teste

### Palavra Aceita: "a1a11" (aa bb)
Entrada: `q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111a111a111Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a11`

Fita final: `sa1a11b#A`

### Palavra Rejeitada: "a1a1a11" (aaa bb)
Entrada: `q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111a111a111Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a1a11`

Fita final: `sa1a1a11b#R`
