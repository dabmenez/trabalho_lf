#!/usr/bin/env python3
"""
Teste completo da Máquina de Turing Universal (MTU)
Simula a execução da MTU para verificar se funciona corretamente
"""

def parse_transicao(transicao):
    """
    Parseia uma transição no formato: <estado><simbolo_lido><simbolo_escrito><movimento><estado_destino>
    Exemplo: q1sa1Rq1 = estado q1, lê s, escreve s, move R, vai para q1
    """
    if not transicao:
        return None
    
    if not transicao.startswith('q'):
        return None
    
    i = 1
    while i < len(transicao) and transicao[i] in '1f':
        i += 1
    
    estado_origem = transicao[:i]
    resto = transicao[i:]
    
    if not resto:
        return None
    
    simbolo_lido = resto[0]  # s, a, b, ou primeiro char do símbolo
    if simbolo_lido == 'a':
        j = 1
        while j < len(resto) and resto[j] == '1':
            j += 1
        simbolo_lido = resto[:j]
        resto = resto[j:]
    else:
        resto = resto[1:]
    
    if not resto:
        return None
    
    simbolo_escrito = resto[0]
    if simbolo_escrito == 'a':
        j = 1
        while j < len(resto) and resto[j] == '1':
            j += 1
        simbolo_escrito = resto[:j]
        resto = resto[j:]
    else:
        resto = resto[1:]
    
    if not resto:
        return None
    
    movimento = resto[0]  # R ou L
    resto = resto[1:]
    
    if not resto:
        return None
    
    estado_destino = resto
    
    return {
        'estado_origem': estado_origem,
        'simbolo_lido': simbolo_lido,
        'simbolo_escrito': simbolo_escrito,
        'movimento': movimento,
        'estado_destino': estado_destino
    }

def simular_mtu(entrada_completa):
    """
    Simula a execução da MTU com uma entrada completa
    Entrada: <codificação_MT>$<palavra_entrada>
    """
    print(f"=== SIMULAÇÃO DA MTU ===")
    print(f"Entrada: {entrada_completa}")
    
    partes = entrada_completa.split('$')
    if len(partes) != 2:
        print("ERRO: Formato de entrada inválido")
        return None
    
    codificacao_mt = partes[0]
    palavra_entrada = partes[1]
    
    print(f"Codificação da MT: {codificacao_mt}")
    print(f"Palavra de entrada: {palavra_entrada}")
    
    transicoes = codificacao_mt.split('#')
    print(f"Transições encontradas: {len(transicoes)}")
    for i, t in enumerate(transicoes):
        print(f"  {i+1}: {t}")
    
    estado_atual = 'q1'  # Estado inicial sempre q1
    fita_mt = list(palavra_entrada + 'b')  # Adicionar símbolo branco
    posicao_mt = 0
    
    print(f"\n=== EXECUÇÃO DA MT SIMULADA ===")
    print(f"Estado inicial: {estado_atual}")
    print(f"Fita inicial: {''.join(fita_mt)}")
    print(f"Posição inicial: {posicao_mt}")
    
    passo = 0
    max_passos = 100
    
    while passo < max_passos:
        if posicao_mt >= len(fita_mt):
            fita_mt.append('b')  # Expandir fita se necessário
        
        simbolo_atual = fita_mt[posicao_mt]
        print(f"\nPasso {passo}: Estado={estado_atual}, Pos={posicao_mt}, Símbolo='{simbolo_atual}'")
        
        transicao_encontrada = None
        for transicao in transicoes:
            if len(transicao) == 0:
                continue
            
            if transicao.startswith(estado_atual):
                resto = transicao[len(estado_atual):]
                
                if resto.startswith(simbolo_atual):
                    transicao_encontrada = transicao
                    break
        
        if transicao_encontrada is None:
            print(f"Nenhuma transição encontrada para estado {estado_atual} e símbolo '{simbolo_atual}'")
            if estado_atual == 'qf':
                print("ACEITA: Parou no estado final")
                resultado = '#A'
            else:
                print("REJEITA: Nenhuma transição aplicável")
                resultado = '#R'
            break
        
        print(f"Transição encontrada: {transicao_encontrada}")
        
        resto = transicao_encontrada[len(estado_atual):]
        simbolo_lido = resto[0] if len(resto) > 0 else ''
        resto = resto[len(simbolo_lido):]
        simbolo_escrito = resto[0] if len(resto) > 0 else ''
        resto = resto[len(simbolo_escrito):]
        movimento = resto[0] if len(resto) > 0 else ''
        estado_destino = resto[1:] if len(resto) > 1 else ''
        
        print(f"  Lê: '{simbolo_lido}', Escreve: '{simbolo_escrito}', Move: '{movimento}', Vai para: '{estado_destino}'")
        
        fita_mt[posicao_mt] = simbolo_escrito
        
        if movimento == 'R':
            posicao_mt += 1
        elif movimento == 'L':
            posicao_mt = max(0, posicao_mt - 1)
        
        estado_atual = estado_destino
        
        print(f"  Nova fita: {''.join(fita_mt)}")
        print(f"  Nova posição: {posicao_mt}")
        print(f"  Novo estado: {estado_atual}")
        
        if estado_atual == 'qf':
            print("ACEITA: Chegou ao estado final")
            resultado = '#A'
            break
        
        passo += 1
    
    if passo >= max_passos:
        print("ERRO: Limite de passos excedido")
        resultado = '#R'
    
    fita_final_mtu = entrada_completa + resultado
    print(f"\n=== RESULTADO FINAL ===")
    print(f"Fita final da MTU: {fita_final_mtu}")
    print(f"Resultado: {'ACEITA' if resultado == '#A' else 'REJEITA'}")
    
    return fita_final_mtu

def main():
    print("=== TESTE COMPLETO DA MTU ===\n")
    
    print("1. TESTE: MT para número par de 'a's")
    print("-" * 50)
    
    mt1_codigo = "q1sa1Rq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf"
    
    entrada1_1 = mt1_codigo + "$sa1a1"
    resultado1_1 = simular_mtu(entrada1_1)
    
    print("\n" + "="*60 + "\n")
    
    entrada1_2 = mt1_codigo + "$sa1"
    resultado1_2 = simular_mtu(entrada1_2)
    
    print("\n" + "="*60 + "\n")
    
    print("2. TESTE: MT para a^n b^n (versão simplificada)")
    print("-" * 50)
    
    mt2_codigo = "q1sa1Rq1#q1a1a111Rq11#q11a11a1111Rqf"
    
    entrada2_1 = mt2_codigo + "$sa1a11"
    resultado2_1 = simular_mtu(entrada2_1)
    
    print("\n" + "="*60 + "\n")
    
    entrada2_2 = mt2_codigo + "$sa1a1"
    resultado2_2 = simular_mtu(entrada2_2)
    
    print("\n" + "="*60 + "\n")
    
    print("=== RESUMO DOS TESTES ===")
    print(f"MT1 + 'sa1a1' (2 a's): {resultado1_1.split('#')[-1]} {'✓' if resultado1_1.endswith('#A') else '✗'}")
    print(f"MT1 + 'sa1' (1 a): {resultado1_2.split('#')[-1]} {'✓' if resultado1_2.endswith('#R') else '✗'}")
    print(f"MT2 + 'sa1a11' (ab): {resultado2_1.split('#')[-1]} {'✓' if resultado2_1.endswith('#A') else '✗'}")
    print(f"MT2 + 'sa1a1' (aa): {resultado2_2.split('#')[-1]} {'✓' if resultado2_2.endswith('#R') else '✗'}")
    
    testes_corretos = (
        resultado1_1.endswith('#A') and  # MT1 deve aceitar número par de a's
        resultado1_2.endswith('#R') and  # MT1 deve rejeitar número ímpar de a's
        resultado2_1.endswith('#A') and  # MT2 deve aceitar ab
        resultado2_2.endswith('#R')      # MT2 deve rejeitar aa
    )
    
    print(f"\nTodos os testes: {'PASSOU ✓' if testes_corretos else 'FALHOU ✗'}")

if __name__ == "__main__":
    main()
