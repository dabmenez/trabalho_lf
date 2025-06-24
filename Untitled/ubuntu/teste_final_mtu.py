#!/usr/bin/env python3
"""
Teste final da Máquina de Turing Universal (MTU)
Versão corrigida com símbolos consistentes
"""

def parse_transicao(transicao):
    """
    Parseia uma transição no formato: <estado><simbolo_lido><simbolo_escrito><movimento><estado_destino>
    """
    if not transicao or not transicao.startswith('q'):
        return None
    
    i = 1
    while i < len(transicao) and transicao[i] in '1f':
        i += 1
    estado_origem = transicao[:i]
    resto = transicao[i:]
    
    if not resto:
        return None
    
    if resto.startswith('a'):
        j = 1
        while j < len(resto) and resto[j] == '1':
            j += 1
        simbolo_lido = resto[:j]
        resto = resto[j:]
    else:
        simbolo_lido = resto[0]  # s, b, etc.
        resto = resto[1:]
    
    if not resto:
        return None
    
    if resto.startswith('a'):
        j = 1
        while j < len(resto) and resto[j] == '1':
            j += 1
        simbolo_escrito = resto[:j]
        resto = resto[j:]
    else:
        simbolo_escrito = resto[0]  # s, b, etc.
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
    
    transicoes_parseadas = []
    for i, t in enumerate(transicoes):
        if t:
            parsed = parse_transicao(t)
            if parsed:
                transicoes_parseadas.append(parsed)
                print(f"  {i+1}: {t} -> {parsed}")
            else:
                print(f"  {i+1}: {t} -> ERRO NO PARSING")
    
    estado_atual = 'q1'
    fita_mt = list(palavra_entrada + 'b')
    posicao_mt = 0
    
    print(f"\n=== EXECUÇÃO DA MT SIMULADA ===")
    print(f"Estado inicial: {estado_atual}")
    print(f"Fita inicial: {''.join(fita_mt)}")
    print(f"Posição inicial: {posicao_mt}")
    
    passo = 0
    max_passos = 50
    
    while passo < max_passos:
        if posicao_mt >= len(fita_mt):
            fita_mt.append('b')
        
        simbolo_atual = fita_mt[posicao_mt]
        print(f"\nPasso {passo}: Estado={estado_atual}, Pos={posicao_mt}, Símbolo='{simbolo_atual}'")
        
        transicao_aplicavel = None
        for t in transicoes_parseadas:
            if t['estado_origem'] == estado_atual and t['simbolo_lido'] == simbolo_atual:
                transicao_aplicavel = t
                break
        
        if transicao_aplicavel is None:
            print(f"Nenhuma transição encontrada para estado {estado_atual} e símbolo '{simbolo_atual}'")
            if estado_atual == 'qf':
                print("ACEITA: Parou no estado final")
                resultado = '#A'
            else:
                print("REJEITA: Nenhuma transição aplicável")
                resultado = '#R'
            break
        
        print(f"Transição aplicável: {transicao_aplicavel}")
        
        fita_mt[posicao_mt] = transicao_aplicavel['simbolo_escrito']
        
        if transicao_aplicavel['movimento'] == 'R':
            posicao_mt += 1
        elif transicao_aplicavel['movimento'] == 'L':
            posicao_mt = max(0, posicao_mt - 1)
        
        estado_atual = transicao_aplicavel['estado_destino']
        
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
    print("=== TESTE FINAL DA MTU ===\n")
    
    print("1. TESTE: MT para número par de 'a1's")
    print("-" * 50)
    
    mt1_codigo = "q1ssRq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf"
    
    print("\nTeste 1.1: Entrada 'sa1a1' (2 a1's - deve aceitar)")
    entrada1_1 = mt1_codigo + "$sa1a1"
    resultado1_1 = simular_mtu(entrada1_1)
    
    print("\n" + "="*60 + "\n")
    
    print("Teste 1.2: Entrada 'sa1' (1 a1 - deve rejeitar)")
    entrada1_2 = mt1_codigo + "$sa1"
    resultado1_2 = simular_mtu(entrada1_2)
    
    print("\n" + "="*60 + "\n")
    
    print("Teste 1.3: Entrada 's' (0 a1's - deve aceitar)")
    entrada1_3 = mt1_codigo + "$s"
    resultado1_3 = simular_mtu(entrada1_3)
    
    print("\n" + "="*60 + "\n")
    
    print("2. TESTE: MT para a1^n a11^n")
    print("-" * 50)
    
    mt2_codigo = "q1ssRq1#q1a1a111Rq11#q11a11a1111Rqf"
    
    print("\nTeste 2.1: Entrada 'sa1a11' (a1 a11 - deve aceitar)")
    entrada2_1 = mt2_codigo + "$sa1a11"
    resultado2_1 = simular_mtu(entrada2_1)
    
    print("\n" + "="*60 + "\n")
    
    print("Teste 2.2: Entrada 'sa1a1' (a1 a1 - deve rejeitar)")
    entrada2_2 = mt2_codigo + "$sa1a1"
    resultado2_2 = simular_mtu(entrada2_2)
    
    print("\n" + "="*60 + "\n")
    
    print("=== RESUMO DOS TESTES ===")
    print(f"MT1 + 'sa1a1' (2 a1's): {resultado1_1.split('#')[-1] if resultado1_1 else 'ERRO'} {'✓' if resultado1_1 and resultado1_1.endswith('#A') else '✗'}")
    print(f"MT1 + 'sa1' (1 a1): {resultado1_2.split('#')[-1] if resultado1_2 else 'ERRO'} {'✓' if resultado1_2 and resultado1_2.endswith('#R') else '✗'}")
    print(f"MT1 + 's' (0 a1's): {resultado1_3.split('#')[-1] if resultado1_3 else 'ERRO'} {'✓' if resultado1_3 and resultado1_3.endswith('#A') else '✗'}")
    print(f"MT2 + 'sa1a11' (aceita): {resultado2_1.split('#')[-1] if resultado2_1 else 'ERRO'} {'✓' if resultado2_1 and resultado2_1.endswith('#A') else '✗'}")
    print(f"MT2 + 'sa1a1' (rejeita): {resultado2_2.split('#')[-1] if resultado2_2 else 'ERRO'} {'✓' if resultado2_2 and resultado2_2.endswith('#R') else '✗'}")
    
    testes_corretos = (
        resultado1_1 and resultado1_1.endswith('#A') and  # MT1 deve aceitar número par de a1's
        resultado1_2 and resultado1_2.endswith('#R') and  # MT1 deve rejeitar número ímpar de a1's
        resultado1_3 and resultado1_3.endswith('#A') and  # MT1 deve aceitar 0 a1's (par)
        resultado2_1 and resultado2_1.endswith('#A') and  # MT2 deve aceitar a1a11
        resultado2_2 and resultado2_2.endswith('#R')      # MT2 deve rejeitar a1a1
    )
    
    print(f"\nTodos os testes: {'PASSOU ✓' if testes_corretos else 'FALHOU ✗'}")
    
    if testes_corretos:
        print("\n🎉 SUCESSO: A simulação da MTU está funcionando corretamente!")
        print("A MTU consegue simular as Máquinas de Turing codificadas e produzir os resultados esperados.")
    else:
        print("\n❌ FALHA: Ainda há problemas na simulação da MTU.")

if __name__ == "__main__":
    main()
