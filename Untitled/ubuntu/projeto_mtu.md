# Projeto Final - Máquina de Turing Universal (MTU)

## 1. Primeira Máquina de Turing: Reconhece palavras com número par de 'a'

### Descrição
Esta MT reconhece palavras que contêm um número par de símbolos 'a' (incluindo zero).

### Estados
- q1: Estado inicial (número par de 'a's encontrados)
- q11: Número ímpar de 'a's encontrados  
- qf: Estado final de aceitação

### Alfabeto
- a1: símbolo 'a'
- b: símbolo branco (fim da entrada)
- s: símbolo de início da fita

### Tabela de Transições

| Estado Atual | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado |
|--------------|--------------|-----------------|-----------|----------------|
| q1           | s            | s               | R         | q1             |
| q1           | a1           | a1              | R         | q11            |
| q1           | b            | b               | R         | qf             |
| q11          | a1           | a1              | R         | q1             |
| q11          | b            | b               | R         | qf             |

### Codificação Unária da MT

Transições codificadas:
1. q1sa1Rq1 → q1sa1Rq1
2. q1a1a1Rq11 → q1a1a1Rq11  
3. q1bb Rqf → q1bbRqf
4. q11a1a1Rq1 → q11a1a1Rq1
5. q11bbRqf → q11bbRqf

Codificação completa:
```
q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf
```

### Palavras de Teste

#### Palavra Aceita: "a1a1" (2 a's - par)
Entrada completa para MTU: `q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1a1`

Execução:
1. Estado q1, lê s → escreve s, move R, vai para q1
2. Estado q1, lê a1 → escreve a1, move R, vai para q11  
3. Estado q11, lê a1 → escreve a1, move R, vai para q1
4. Estado q1, lê b → escreve b, move R, vai para qf

Fita final: `sa1a1b#A`

#### Palavra Rejeitada: "a1" (1 a - ímpar)
Entrada completa para MTU: `q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1`

Execução:
1. Estado q1, lê s → escreve s, move R, vai para q1
2. Estado q1, lê a1 → escreve a1, move R, vai para q11
3. Estado q11, lê b → escreve b, move R, vai para qf (mas q11 não é estado final)

Como q11 não é estado final, a palavra é rejeitada.
Fita final: `sa1b#R`
