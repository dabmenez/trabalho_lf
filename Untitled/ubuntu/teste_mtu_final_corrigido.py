#!/usr/bin/env python3
"""
Teste final corrigido da Máquina de Turing Universal (MTU)
Versão que resolve o problema de codificação de símbolos
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

def converter_entrada_para_unario(entrada):
    """
    Converte entrada com símbolos simples para formato unário
    'a' -> 'a1', 'aa' -> 'a1a1', etc.
    """
    resultado = ""
    for char in entrada:
        if char == 'a':
            resultado += 'a1'
        elif char == 'b':
            resultado += 'a11'  # 'b' é representado como 'a11' na codificação unária
        else:
            resultado += char  # 's', 'b' (branco), etc. permanecem iguais
    return resultado

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
    print(f"Palavra de entrada original: {palavra_entrada}")
    
    palavra_entrada_unaria = converter_entrada_para_unario(palavra_entrada)
    print(f"Palavra de entrada em unário: {palavra_entrada_unaria}")
    
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
    fita_mt = list(palavra_entrada_unaria + 'b')
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
        
        if posicao_mt < len(fita_mt):
            simbolo_atual = fita_mt[posicao_mt]
            if simbolo_atual == 'a' and posicao_mt + 1 < len(fita_mt):
                j = posicao_mt + 1
                while j < len(fita_mt) and fita_mt[j] == '1':
                    j += 1
                simbolo_atual = ''.join(fita_mt[posicao_mt:j])
        else:
            simbolo_atual = 'b'
        
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
        
        simbolo_escrito = transicao_aplicavel['simbolo_escrito']
        simbolo_lido = transicao_aplicavel['simbolo_lido']
        
        if simbolo_lido.startswith('a') and len(simbolo_lido) > 1:
            for _ in range(len(simbolo_lido)):
                if posicao_mt < len(fita_mt):
                    fita_mt.pop(posicao_mt)
        else:
            if posicao_mt < len(fita_mt):
                fita_mt.pop(posicao_mt)
        
        if simbolo_escrito.startswith('a') and len(simbolo_escrito) > 1:
            for i, char in enumerate(simbolo_escrito):
                fita_mt.insert(posicao_mt + i, char)
        else:
            fita_mt.insert(posicao_mt, simbolo_escrito)
        
        if transicao_aplicavel['movimento'] == 'R':
            posicao_mt += len(simbolo_escrito) if simbolo_escrito.startswith('a') and len(simbolo_escrito) > 1 else 1
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
    print("=== TESTE FINAL CORRIGIDO DA MTU ===\n")
    
    print("1. TESTE: MT para número par de 'a's")
    print("-" * 50)
    
    mt1_codigo = "q1ssRq1#q1a1a1Rq11#q1bbRqf#q11a1a1Rq1#q11bbRqf"
    
    print("\nTeste 1.1: Entrada 'saa' (2 a's - deve aceitar)")
    entrada1_1 = mt1_codigo + "$saa"
    resultado1_1 = simular_mtu(entrada1_1)
    
    print("\n" + "="*60 + "\n")
    
    print("Teste 1.2: Entrada 'sa' (1 a - deve rejeitar)")
    entrada1_2 = mt1_codigo + "$sa"
    resultado1_2 = simular_mtu(entrada1_2)
    
    print("\n" + "="*60 + "\n")
    
    print("Teste 1.3: Entrada 's' (0 a's - deve aceitar)")
    entrada1_3 = mt1_codigo + "$s"
    resultado1_3 = simular_mtu(entrada1_3)
    
    print("\n" + "="*60 + "\n")
    
    print("=== RESUMO DOS TESTES ===")
    print(f"MT1 + 'saa' (2 a's): {resultado1_1.split('#')[-1] if resultado1_1 else 'ERRO'} {'✓' if resultado1_1 and resultado1_1.endswith('#A') else '✗'}")
    print(f"MT1 + 'sa' (1 a): {resultado1_2.split('#')[-1] if resultado1_2 else 'ERRO'} {'✓' if resultado1_2 and resultado1_2.endswith('#R') else '✗'}")
    print(f"MT1 + 's' (0 a's): {resultado1_3.split('#')[-1] if resultado1_3 else 'ERRO'} {'✓' if resultado1_3 and resultado1_3.endswith('#A') else '✗'}")
    
    testes_corretos = (
        resultado1_1 and resultado1_1.endswith('#A') and  # MT1 deve aceitar número par de a's
        resultado1_2 and resultado1_2.endswith('#R') and  # MT1 deve rejeitar número ímpar de a's
        resultado1_3 and resultado1_3.endswith('#A')      # MT1 deve aceitar 0 a's (par)
    )
    
    print(f"\nTodos os testes: {'PASSOU ✓' if testes_corretos else 'FALHOU ✗'}")
    
    if testes_corretos:
        print("\n🎉 SUCESSO: A simulação da MTU está funcionando corretamente!")
        print("A MTU consegue simular a Máquina de Turing para número par de 'a's.")
        print("\n📋 VALIDAÇÃO COMPLETA:")
        print("✅ Parsing de transições unárias funcionando")
        print("✅ Conversão de entrada para formato unário")
        print("✅ Simulação de execução da MT")
        print("✅ Detecção correta de aceitação/rejeição")
        print("✅ Formato de saída (#A/#R) correto")
    else:
        print("\n❌ FALHA: Ainda há problemas na simulação da MTU.")

if __name__ == "__main__":
    main()
