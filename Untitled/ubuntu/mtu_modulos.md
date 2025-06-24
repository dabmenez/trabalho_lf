# Máquina de Turing Universal (MTU) - Módulos

## Visão Geral da MTU

A MTU é composta por 4 módulos principais que trabalham em sequência:

1. **Módulo Localizar Transição**: Encontra a transição aplicável ao estado atual e símbolo lido
2. **Módulo Aplicar Transição**: Executa a transição (escreve símbolo, move cabeçote, atualiza estado)
3. **Módulo Verificar Aceitação**: Verifica se chegou ao estado final qf
4. **Módulo Verificar Rejeição**: Verifica se não há transição aplicável

## Estados da MTU

### Estados de Controle Principal
- q1: Estado inicial da MTU
- q_busca: Iniciando busca por transição
- q_encontrou: Transição encontrada
- q_aplica: Aplicando transição
- q_verifica_final: Verificando se é estado final
- q_aceita: Escreve #A e para
- q_rejeita: Escreve #R e para
- qf: Estado final da MTU

### Estados Auxiliares para Navegação
- q_volta_inicio: Voltando ao início da codificação
- q_avanca_entrada: Avançando para a entrada
- q_busca_estado: Buscando estado na transição
- q_busca_simbolo: Buscando símbolo na transição
- q_copia_simbolo: Copiando símbolo para escrita
- q_move_cabecote: Movendo cabeçote da MT simulada

## Módulo 1: Localizar Transição Válida

### Função
Percorre a codificação da MT para encontrar uma transição que corresponda ao estado atual e símbolo sendo lido pela MT simulada.

### Estados do Módulo
- q_busca: Estado inicial do módulo
- q_compara_estado: Comparando estado da transição com estado atual
- q_compara_simbolo: Comparando símbolo da transição com símbolo lido
- q_transicao_valida: Transição válida encontrada
- q_proxima_transicao: Avançar para próxima transição
- q_nao_encontrou: Nenhuma transição aplicável

### Tabela de Transições do Módulo 1

| Estado | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado | Descrição |
|--------|--------------|-----------------|-----------|----------------|-----------|
| q_busca | q | q | R | q_compara_estado | Início de transição encontrada |
| q_compara_estado | 1 | 1 | R | q_compara_estado | Contando 1s do estado |
| q_compara_estado | a | a | R | q_compara_simbolo | Estado conferido, verificar símbolo |
| q_compara_simbolo | 1 | 1 | R | q_compara_simbolo | Contando 1s do símbolo |
| q_compara_simbolo | a | a | R | q_transicao_valida | Símbolo conferido, transição válida |
| q_busca | # | # | R | q_proxima_transicao | Pular para próxima transição |
| q_proxima_transicao | q | q | L | q_busca | Voltar para buscar |
| q_busca | $ | $ | L | q_nao_encontrou | Fim das transições, nenhuma válida |

### Como Funciona
1. Inicia no estado q_busca
2. Procura por 'q' (início de transição)
3. Compara o estado da transição com o estado atual da MT simulada
4. Se estados coincidem, compara o símbolo
5. Se símbolos coincidem, transição é válida
6. Se não coincidem, avança para próxima transição
7. Se chegou ao '$', nenhuma transição é aplicável

### Conexão com Próximo Módulo
- Se transição válida encontrada → vai para Módulo 2 (Aplicar Transição)
- Se nenhuma transição encontrada → vai para Módulo 4 (Verificar Rejeição)

## Módulo 2: Aplicar Transição

### Função
Executa a transição encontrada: escreve o símbolo especificado, move o cabeçote e atualiza o estado atual.

### Estados do Módulo
- q_aplica: Estado inicial do módulo
- q_le_simbolo_escrever: Lendo símbolo a ser escrito
- q_le_movimento: Lendo direção do movimento
- q_le_estado_destino: Lendo estado destino
- q_escreve_simbolo: Escrevendo símbolo na fita
- q_move_direita: Movendo cabeçote para direita
- q_move_esquerda: Movendo cabeçote para esquerda
- q_atualiza_estado: Atualizando estado atual

### Tabela de Transições do Módulo 2

| Estado | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado | Descrição |
|--------|--------------|-----------------|-----------|----------------|-----------|
| q_aplica | a | a | R | q_le_simbolo_escrever | Pular símbolo lido |
| q_le_simbolo_escrever | a | a | R | q_le_movimento | Símbolo a escrever identificado |
| q_le_movimento | R | R | R | q_le_estado_destino | Movimento para direita |
| q_le_movimento | L | L | R | q_le_estado_destino | Movimento para esquerda |
| q_le_estado_destino | q | q | R | q_escreve_simbolo | Estado destino identificado |
| q_escreve_simbolo | [símbolo] | [novo_símbolo] | N | q_move_direita | Escrever símbolo |
| q_move_direita | [qualquer] | [qualquer] | R | q_atualiza_estado | Mover direita |
| q_move_esquerda | [qualquer] | [qualquer] | L | q_atualiza_estado | Mover esquerda |

### Como Funciona
1. Posiciona na transição válida encontrada
2. Lê o símbolo a ser escrito
3. Lê a direção do movimento (R ou L)
4. Lê o estado destino
5. Vai até a posição atual na entrada e escreve o novo símbolo
6. Move o cabeçote conforme especificado
7. Atualiza o estado atual da MT simulada

### Conexão com Próximo Módulo
Sempre vai para Módulo 3 (Verificar Aceitação)

## Módulo 3: Verificar Parada por Aceitação

### Função
Verifica se o estado atual da MT simulada é o estado final 'qf'.

### Estados do Módulo
- q_verifica_final: Estado inicial do módulo
- q_le_estado_atual: Lendo estado atual
- q_compara_qf: Comparando com qf
- q_eh_final: Estado atual é qf
- q_nao_final: Estado atual não é qf

### Tabela de Transições do Módulo 3

| Estado | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado | Descrição |
|--------|--------------|-----------------|-----------|----------------|-----------|
| q_verifica_final | q | q | R | q_le_estado_atual | Início do estado atual |
| q_le_estado_atual | f | f | N | q_eh_final | Estado atual é qf |
| q_le_estado_atual | 1 | 1 | R | q_nao_final | Estado atual não é qf |
| q_eh_final | [qualquer] | [qualquer] | N | q_aceita | Ir para aceitação |
| q_nao_final | [qualquer] | [qualquer] | N | q_busca | Voltar para buscar transição |

### Como Funciona
1. Localiza o estado atual da MT simulada
2. Verifica se é 'qf' (estado final)
3. Se for qf, vai para estado de aceitação
4. Se não for qf, volta para buscar nova transição

### Conexão com Próximo Módulo
- Se estado atual é qf → escreve #A e para
- Se estado atual não é qf → volta para Módulo 1 (Localizar Transição)

## Módulo 4: Verificar Parada por Rejeição

### Função
Escreve #R quando não há transição aplicável (rejeição).

### Estados do Módulo
- q_rejeita: Estado do módulo
- q_escreve_R: Escrevendo #R

### Tabela de Transições do Módulo 4

| Estado | Símbolo Lido | Símbolo Escrito | Movimento | Próximo Estado | Descrição |
|--------|--------------|-----------------|-----------|----------------|-----------|
| q_rejeita | b | # | R | q_escreve_R | Escrever # |
| q_escreve_R | b | R | N | qf | Escrever R e parar |

### Como Funciona
1. Posiciona após a entrada
2. Escreve '#R'
3. Para a execução

### Conexão
Este é o módulo final para rejeição - para a MTU.

## Fluxo de Execução da MTU

1. **Inicialização**: MTU inicia no estado q1
2. **Loop Principal**:
   - Módulo 1: Localizar transição válida
   - Se encontrou → Módulo 2: Aplicar transição
   - Módulo 3: Verificar se é estado final
   - Se não é final → volta para Módulo 1
   - Se é final → escreve #A e para
   - Se não encontrou transição → Módulo 4: escreve #R e para

## Orientações para Implementação no JFLAP

1. **Estrutura Modular**: Implemente cada módulo como um conjunto de estados conectados
2. **Estados de Controle**: Use estados intermediários para controlar o fluxo entre módulos
3. **Navegação na Fita**: Implemente estados para mover o cabeçote para diferentes partes da entrada
4. **Marcação de Posição**: Use símbolos especiais para marcar posições importantes na fita
5. **Teste Incremental**: Teste cada módulo separadamente antes de conectar todos

## Conexão dos Módulos

```
Início → Módulo 1 (Localizar) → Módulo 2 (Aplicar) → Módulo 3 (Verificar Final)
                ↓                                            ↓
         Módulo 4 (Rejeitar)                          ← ← ← ← ←
                ↓                                            
              FIM                                     (se não final)
```
