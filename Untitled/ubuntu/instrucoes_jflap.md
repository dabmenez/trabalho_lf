# Instruções para Reconstrução da MTU no JFLAP

## Visão Geral da Implementação

A Máquina de Turing Universal (MTU) foi projetada com arquitetura modular para facilitar a implementação e depuração no JFLAP. A MTU simula qualquer Máquina de Turing determinística seguindo o formato de codificação especificado.

## Estrutura Modular da MTU

### Módulo 1: Localizar Transição Válida
**Estados:** q_busca_transicao, q_compara_estado, q_compara_simbolo, q_transicao_valida, q_proxima_transicao, q_nao_encontrou

**Função:** Percorre a codificação da MT para encontrar uma transição aplicável ao estado atual e símbolo sendo lido.

**Fluxo:**
1. Inicia em q_busca_transicao
2. Procura por 'q' (início de transição)
3. Compara estado da transição com estado atual da MT simulada
4. Se estados coincidem, compara símbolo lido
5. Se símbolos coincidem, transição é válida → vai para Módulo 2
6. Se não coincidem, avança para próxima transição
7. Se chegou ao '$', nenhuma transição aplicável → vai para Módulo 4

### Módulo 2: Aplicar Transição
**Estados:** q_aplica_transicao, q_le_simbolo_escrever, q_le_movimento, q_le_estado_destino, q_executa_transicao

**Função:** Executa a transição encontrada (escreve símbolo, move cabeçote, atualiza estado).

**Fluxo:**
1. Lê símbolo a ser escrito da transição
2. Lê direção do movimento (R ou L)
3. Lê estado destino
4. Vai até posição atual na entrada
5. Escreve novo símbolo
6. Move cabeçote conforme especificado
7. Atualiza estado atual → vai para Módulo 3

### Módulo 3: Verificar Aceitação
**Estados:** q_verifica_final, q_eh_final, q_nao_final

**Função:** Verifica se o estado atual da MT simulada é o estado final 'qf'.

**Fluxo:**
1. Localiza estado atual da MT simulada
2. Se é 'qf' → vai para Módulo de Aceitação (escreve #A)
3. Se não é 'qf' → volta para Módulo 1 (buscar nova transição)

### Módulo 4: Parada por Rejeição
**Estados:** q_rejeita, q_escreve_R

**Função:** Escreve #R quando não há transição aplicável.

**Fluxo:**
1. Posiciona após a entrada
2. Escreve '#R'
3. Para a execução (vai para qf)

## Passos para Implementação no JFLAP

### Passo 1: Criar Estados
1. Abra o JFLAP e crie uma nova Máquina de Turing
2. Adicione os seguintes estados principais:
   - q_inicio (inicial)
   - q_busca_transicao
   - q_compara_estado
   - q_compara_simbolo
   - q_transicao_valida
   - q_proxima_transicao
   - q_nao_encontrou
   - q_aplica_transicao
   - q_le_simbolo_escrever
   - q_le_movimento
   - q_le_estado_destino
   - q_executa_transicao
   - q_verifica_final
   - q_eh_final
   - q_nao_final
   - q_aceita
   - q_rejeita
   - q_escreve_A
   - q_escreve_R
   - qf (final)

### Passo 2: Adicionar Estados Auxiliares
Para navegação na fita:
   - q_volta_inicio
   - q_vai_entrada
   - q_marca_posicao
   - q_busca_estado_atual
   - q_busca_simbolo_atual

### Passo 3: Implementar Transições do Módulo 1

#### Inicialização
```
q_inicio → q_busca_transicao (lê: q, escreve: q, move: R)
```

#### Busca de Transição
```
q_busca_transicao → q_compara_estado (lê: q, escreve: q, move: R)
q_busca_transicao → q_proxima_transicao (lê: #, escreve: #, move: R)
q_busca_transicao → q_nao_encontrou (lê: $, escreve: $, move: L)
```

#### Comparação de Estado
```
q_compara_estado → q_compara_estado (lê: 1, escreve: 1, move: R)
q_compara_estado → q_compara_estado (lê: f, escreve: f, move: R)
q_compara_estado → q_compara_simbolo (lê: a, escreve: a, move: R)
q_compara_estado → q_compara_simbolo (lê: b, escreve: b, move: R)
q_compara_estado → q_compara_simbolo (lê: s, escreve: s, move: R)
```

#### Comparação de Símbolo
```
q_compara_simbolo → q_compara_simbolo (lê: 1, escreve: 1, move: R)
q_compara_simbolo → q_transicao_valida (lê: a, escreve: a, move: R)
q_compara_simbolo → q_transicao_valida (lê: b, escreve: b, move: R)
q_compara_simbolo → q_transicao_valida (lê: s, escreve: s, move: R)
```

#### Próxima Transição
```
q_proxima_transicao → q_busca_transicao (lê: q, escreve: q, move: L)
```

### Passo 4: Implementar Transições do Módulo 2

#### Aplicar Transição
```
q_transicao_valida → q_aplica_transicao (lê: a, escreve: a, move: R)
q_transicao_valida → q_aplica_transicao (lê: b, escreve: b, move: R)
q_transicao_valida → q_aplica_transicao (lê: s, escreve: s, move: R)
```

#### Ler Elementos da Transição
```
q_aplica_transicao → q_le_simbolo_escrever (lê: 1, escreve: 1, move: R)
q_le_simbolo_escrever → q_le_movimento (lê: a, escreve: a, move: R)
q_le_simbolo_escrever → q_le_movimento (lê: b, escreve: b, move: R)
q_le_simbolo_escrever → q_le_movimento (lê: s, escreve: s, move: R)
q_le_movimento → q_le_estado_destino (lê: R, escreve: R, move: R)
q_le_movimento → q_le_estado_destino (lê: L, escreve: L, move: R)
q_le_estado_destino → q_executa_transicao (lê: q, escreve: q, move: R)
```

### Passo 5: Implementar Transições do Módulo 3

#### Verificar Estado Final
```
q_executa_transicao → q_verifica_final (lê: 1, escreve: 1, move: R)
q_executa_transicao → q_verifica_final (lê: f, escreve: f, move: R)
q_verifica_final → q_eh_final (lê: f, escreve: f, move: N)
q_verifica_final → q_nao_final (lê: 1, escreve: 1, move: N)
q_eh_final → q_aceita (qualquer símbolo)
q_nao_final → q_busca_transicao (qualquer símbolo)
```

### Passo 6: Implementar Transições do Módulo 4

#### Estados de Parada
```
q_nao_encontrou → q_rejeita (qualquer símbolo)
q_aceita → q_escreve_A (lê: b, escreve: #, move: R)
q_escreve_A → qf (lê: b, escreve: A, move: N)
q_rejeita → q_escreve_R (lê: b, escreve: #, move: R)
q_escreve_R → qf (lê: b, escreve: R, move: N)
```

## Dicas para Implementação

### 1. Teste Incremental
- Implemente um módulo por vez
- Teste cada módulo separadamente antes de conectar
- Use entradas simples para verificar funcionamento

### 2. Navegação na Fita
- Implemente estados auxiliares para mover o cabeçote
- Use símbolos especiais para marcar posições importantes
- Mantenha controle da posição atual na entrada

### 3. Depuração
- Use o modo "Step" do JFLAP para acompanhar execução
- Verifique se as comparações de estado e símbolo estão corretas
- Confirme que as transições levam aos estados corretos

### 4. Otimização
- Combine transições similares quando possível
- Use transições com movimento "N" (nenhum) para economizar estados
- Agrupe verificações relacionadas

## Formato de Entrada para Testes

### Entrada Básica
```
q1a1a1Rq11#q11a1a1Rq1#q1bbRqf#q11bbRqf$sa1a1
```

### Componentes
- **Transições:** q1a1a1Rq11#q11a1a1Rq1#q1bbRqf#q11bbRqf
- **Separador:** $
- **Entrada:** sa1a1

### Resultado Esperado
- **Aceitação:** Fita termina com #A
- **Rejeição:** Fita termina com #R

## Verificação Final

1. **Teste com MT1 (número par de a's):**
   - Entrada aceita: sa1a1 → deve resultar em #A
   - Entrada rejeitada: sa1 → deve resultar em #R

2. **Teste com MT2 (a^n b^n):**
   - Entrada aceita: sa1a11 → deve resultar em #A
   - Entrada rejeitada: sa1a1a11 → deve resultar em #R

3. **Verificar modularidade:**
   - Cada módulo deve funcionar independentemente
   - Fluxo entre módulos deve ser correto
   - Estados de parada devem ser alcançados

A implementação completa da MTU no JFLAP seguindo estas instruções deve ser capaz de simular qualquer Máquina de Turing determinística codificada no formato especificado.
