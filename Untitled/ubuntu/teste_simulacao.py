#!/usr/bin/env python3
"""
Simulador para testar as Máquinas de Turing antes da implementação da MTU
"""

def simular_mt_par_as(entrada):
    """
    Simula a MT que reconhece palavras com número par de 'a's
    """
    estado = 'q1'
    fita = list('s' + entrada + 'b')
    posicao = 0
    
    print(f"Simulando MT para número par de 'a's")
    print(f"Entrada: {entrada}")
    print(f"Fita inicial: {''.join(fita)}")
    print(f"Estado inicial: {estado}, Posição: {posicao}")
    print()
    
    passo = 0
    while estado != 'qf' and passo < 100:  # limite para evitar loop infinito
        simbolo_atual = fita[posicao]
        print(f"Passo {passo}: Estado={estado}, Posição={posicao}, Símbolo='{simbolo_atual}'")
        
        if estado == 'q1':
            if simbolo_atual == 's':
                fita[posicao] = 's'
                posicao += 1
                estado = 'q1'
            elif simbolo_atual == 'a':
                fita[posicao] = 'a'
                posicao += 1
                estado = 'q11'
            elif simbolo_atual == 'b':
                fita[posicao] = 'b'
                posicao += 1
                estado = 'qf'
            else:
                print(f"Erro: símbolo não reconhecido '{simbolo_atual}'")
                break
                
        elif estado == 'q11':
            if simbolo_atual == 'a':
                fita[posicao] = 'a'
                posicao += 1
                estado = 'q1'
            elif simbolo_atual == 'b':
                fita[posicao] = 'b'
                posicao += 1
                estado = 'qf'  # Mas q11 não é estado final, então será rejeitado
            else:
                print(f"Erro: símbolo não reconhecido '{simbolo_atual}'")
                break
        
        passo += 1
    
    if estado == 'qf':
        num_as = entrada.count('a')
        if num_as % 2 == 0:
            resultado = '#A'
            print(f"ACEITA: Número par de 'a's ({num_as})")
        else:
            resultado = '#R'
            print(f"REJEITA: Parou em estado não-final após número ímpar de 'a's ({num_as})")
    else:
        resultado = '#R'
        print(f"REJEITA: Não chegou ao estado final")
    
    fita_final = ''.join(fita) + resultado
    print(f"Fita final: {fita_final}")
    print()
    return fita_final

def simular_mt_aa_bb(entrada):
    """
    Simula a MT que reconhece a^n b^n (aa seguido de bb)
    """
    estado = 'q1'
    fita = list('s' + entrada + 'b')
    posicao = 0
    
    print(f"Simulando MT para a^n b^n")
    print(f"Entrada: {entrada}")
    print(f"Fita inicial: {''.join(fita)}")
    print(f"Estado inicial: {estado}, Posição: {posicao}")
    print()
    
    passo = 0
    while estado != 'qf' and passo < 100:  # limite para evitar loop infinito
        if posicao >= len(fita):
            fita.append('b')  # Expandir fita se necessário
        
        simbolo_atual = fita[posicao]
        print(f"Passo {passo}: Estado={estado}, Posição={posicao}, Símbolo='{simbolo_atual}'")
        
        if estado == 'q1':
            if simbolo_atual == 's':
                fita[posicao] = 's'
                posicao += 1
                estado = 'q1'
            elif simbolo_atual == 'a':
                fita[posicao] = 'X'  # Marcar 'a'
                posicao += 1
                estado = 'q11'
            elif simbolo_atual == 'b':
                estado = 'qf'  # Mas não é aceitação válida
                break
            else:
                break
                
        elif estado == 'q11':
            if simbolo_atual == 'a':
                fita[posicao] = 'a'
                posicao += 1
                estado = 'q11'
            elif simbolo_atual == 'b':
                fita[posicao] = 'Y'  # Marcar 'b'
                posicao -= 1
                estado = 'q111'
            else:
                break
                
        elif estado == 'q111':
            if simbolo_atual == 'a':
                fita[posicao] = 'a'
                posicao -= 1
                estado = 'q111'
            elif simbolo_atual == 'X':
                fita[posicao] = 'X'
                posicao -= 1
                estado = 'q111'
            elif simbolo_atual == 's':
                fita[posicao] = 's'
                posicao += 1
                estado = 'q1111'
            else:
                break
                
        elif estado == 'q1111':
            if simbolo_atual == 'X':
                fita[posicao] = 'X'
                posicao += 1
                estado = 'q1111'
            elif simbolo_atual == 'a':
                fita[posicao] = 'X'
                posicao += 1
                estado = 'q11'
            elif simbolo_atual == 'Y':
                fita[posicao] = 'Y'
                posicao += 1
                estado = 'q1111'
            elif simbolo_atual == 'b':
                fita[posicao] = 'b'
                posicao += 1
                estado = 'qf'
            else:
                break
        
        passo += 1
    
    if estado == 'qf':
        num_as = entrada.count('a')
        num_bs = entrada.count('b')
        if num_as > 0 and num_as == num_bs and entrada == 'a' * num_as + 'b' * num_bs:
            resultado = '#A'
            print(f"ACEITA: Entrada válida a^{num_as} b^{num_bs}")
        else:
            resultado = '#R'
            print(f"REJEITA: Entrada inválida")
    else:
        resultado = '#R'
        print(f"REJEITA: Não chegou ao estado final")
    
    fita_final = ''.join(fita) + resultado
    print(f"Fita final: {fita_final}")
    print()
    return fita_final

def main():
    print("=== TESTE DAS MÁQUINAS DE TURING ===\n")
    
    print("1. MÁQUINA PARA NÚMERO PAR DE 'a's")
    print("-" * 40)
    
    casos_mt1 = [
        "",        # 0 a's (par) - deve aceitar
        "a",       # 1 a (ímpar) - deve rejeitar  
        "aa",      # 2 a's (par) - deve aceitar
        "aaa",     # 3 a's (ímpar) - deve rejeitar
        "aaaa",    # 4 a's (par) - deve aceitar
    ]
    
    for caso in casos_mt1:
        simular_mt_par_as(caso)
    
    print("\n2. MÁQUINA PARA a^n b^n")
    print("-" * 40)
    
    casos_mt2 = [
        "ab",      # a^1 b^1 - deve aceitar
        "aabb",    # a^2 b^2 - deve aceitar
        "aaabbb",  # a^3 b^3 - deve aceitar
        "aab",     # a^2 b^1 - deve rejeitar
        "abb",     # a^1 b^2 - deve rejeitar
        "abab",    # intercalado - deve rejeitar
        "",        # vazio - deve rejeitar
        "a",       # só a's - deve rejeitar
        "b",       # só b's - deve rejeitar
    ]
    
    for caso in casos_mt2:
        simular_mt_aa_bb(caso)

if __name__ == "__main__":
    main()
