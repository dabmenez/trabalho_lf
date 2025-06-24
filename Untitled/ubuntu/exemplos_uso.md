# Exemplos de Uso da MTU

## Exemplo 1: MT que reconhece número par de 'a's

### Codificação da MT (CORRIGIDA)
```
q1ssRq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRq111#q111a1a1Rq111#q111bbRq111#q111ssRq111
```

### Lógica da MT
- **q1** (estado par): Lê 's' mantém q1, lê 'a1' vai para q11, lê 'b' vai para qf (aceita)
- **q11** (estado ímpar): Lê 'a1' vai para q1, lê 'b' vai para q111 (rejeita)  
- **q111** (estado de rejeição): Qualquer símbolo permanece em q111 (loop infinito = rejeição)

### Teste 1: Palavra aceita "a1a1" (2 a's - par)
**Entrada completa para MTU:**
```
q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1a1
```

**Execução passo a passo:**
1. MTU inicia no estado q_inicio
2. Localiza primeira transição: q1sa1Rq1
3. Estado atual da MT simulada: q1, Símbolo atual: s
4. Transição encontrada: q1sa1Rq1 (estado q1, lê s, escreve s, move R, vai para q1)
5. Aplica transição: escreve s, move direita, atualiza estado para q1
6. Verifica se é estado final: q1 não é qf, continua
7. Localiza próxima transição aplicável: q1a1a1Rq11
8. Aplica transição: escreve a1, move direita, atualiza estado para q11
9. Localiza próxima transição aplicável: q11a1a1Rq1
10. Aplica transição: escreve a1, move direita, atualiza estado para q1
11. Localiza próxima transição aplicável: q1bbRqf
12. Aplica transição: escreve b, move direita, atualiza estado para qf
13. Verifica se é estado final: qf é estado final
14. Escreve #A após a entrada

**Fita final:**
```
q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1a1#A
```

### Teste 2: Palavra rejeitada "a1" (1 a - ímpar)
**Entrada completa para MTU:**
```
q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1
```

**Execução passo a passo:**
1. MTU inicia no estado q_inicio
2. Localiza primeira transição: q1sa1Rq1
3. Aplica transição: escreve s, move direita, estado q1
4. Localiza próxima transição: q1a1a1Rq11
5. Aplica transição: escreve a1, move direita, estado q11
6. Localiza próxima transição: q11bbRqf
7. Aplica transição: escreve b, move direita, estado qf
8. Verifica estado: qf é final, mas a MT simulada parou em estado q11 (não final)
9. Como q11 não é estado final da MT original, a palavra é rejeitada
10. Escreve #R após a entrada

**Fita final:**
```
q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf$sa1#R
```

## Exemplo 2: MT que reconhece a^n b^n

### Codificação da MT (simplificada)
```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf
```

### Teste 1: Palavra aceita "a1a11" (ab)
**Entrada completa para MTU:**
```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a11
```

**Fita final esperada:**
```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a11#A
```

### Teste 2: Palavra rejeitada "a1a1a11" (aab)
**Entrada completa para MTU:**
```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a1a11
```

**Fita final esperada:**
```
q1sa1Rq1#q1a1a111Rq11#q11a1a1Rq11#q11a11a1111Lq111#q111a1a1Lq111#q111sa1Rq1111#q1111a111a111Rq1111#q1111a1a111Rq11#q1111a1111a1111Rq1111#q1111bbRqf$sa1a1a11#R
```

## Formato de Entrada para a MTU

### Estrutura Geral
```
<transição1>#<transição2>#...#<última_transição>$<palavra_entrada>
```

### Formato de Cada Transição
```
<estado_origem><símbolo_lido><símbolo_escrito><movimento><estado_destino>
```

### Codificação dos Elementos

#### Estados
- Estado inicial: q1
- Estados numerados: q11, q111, q1111, ... (notação unária)
- Estado final: qf

#### Símbolos
- Símbolo 'a': a1
- Símbolo 'b': a11
- Outros símbolos: a111, a1111, ... (notação unária)
- Símbolo branco: b
- Símbolo de início: s

#### Movimentos
- Direita: R
- Esquerda: L

### Separadores
- Entre transições: #
- Entre MT e entrada: $

## Instruções para Uso no JFLAP

1. **Importar o arquivo MTU**: Abra o arquivo `mtu_completa.jff` no JFLAP
2. **Preparar entrada**: Formate a entrada conforme os exemplos acima
3. **Executar simulação**: Use a função "Input" do JFLAP para inserir a entrada
4. **Verificar resultado**: A fita final deve mostrar #A (aceita) ou #R (rejeita)

## Verificação dos Resultados

### Para Aceitação (#A)
- A MTU para no estado final qf
- A fita contém #A após a palavra de entrada
- Indica que a MT simulada aceitou a entrada

### Para Rejeição (#R)
- A MTU para no estado final qf
- A fita contém #R após a palavra de entrada
- Indica que a MT simulada rejeitou a entrada (não há transição aplicável)
