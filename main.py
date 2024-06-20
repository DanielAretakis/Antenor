import re
import sys

def leArquivo():
    try:
        with open(sys.argv[1], "r") as arquivo:
            automato = arquivo.readlines()
        return automato
    except FileNotFoundError:
        print("Arquivo nao encontrado!!!!!!!!!!.")
        sys.exit(1)

def limpaPrimeiraLinha(automato):
    primeira_linha = automato[0]
    regex = re.compile(r'\{[^\}]*\}')
    dados = re.findall(regex, primeira_linha)
    result = [elemento.strip("{}").replace(" ", "").split(",") for elemento in dados]
    return result

def buscaEstadoInicial(automato):
    primeira_linha = automato[0]
    regex = re.compile(r"Z|,\sq\w*,\s{")
    dado = re.findall(regex, primeira_linha)
    estado_inicial = [elemento.strip(",{ ") for elemento in dado]
    return estado_inicial

def leRegrasDeTransicao(automato):
    regras = [linha.strip("\n").replace(" ", "").split(",") for linha in automato[1:]]
    return regras

def leituraDaPalavra(estado_inicial, estados_finais, regras):
    palavra = sys.argv[2]
    estado_atual = estado_inicial[0]

    if palavra == "&":
        return estado_atual in estados_finais
    
    i = 0
    while i < len(palavra):
        letra = palavra[i]

        if letra == '&':
            i += 1
            continue
        
        validacao = False

        for regra in regras:
            regra_estado_entrada, regra_letra, regra_estado_saida = regra
            if regra_estado_entrada == estado_atual and (regra_letra == letra or regra_letra == '&'):
                print(f"({estado_atual}, {palavra[i:]}) = {regra_estado_saida}")
                estado_atual = regra_estado_saida
                validacao = True
                break

        if not validacao:
            print(f"Não há transição válida para a letra '{letra}' a partir do estado '{estado_atual}'.")
            return False

        i += 1

    return estado_atual in estados_finais

def automatoValido(alfabeto, estados, estados_finais, regras):
    if not estados[0]:
        print("\nO conjunto de estados deve ser >= 1\nAPRESENTE UM ARQUIVO VÁLIDO")
        return False
    for estado in estados_finais:
        if estado not in estados:
            print(f"\nEstado Final {estado}\nnão está no conjunto de estados possíveis do automato {estados}\nAPRESENTE UM ARQUIVO VÁLIDO")
            return False

    for regra in regras:
        regra_estado_entrada, regra_letra, regra_estado_saida = regra
        if regra_estado_entrada not in estados:
            print(f"\nEstado {regra_estado_entrada} da regra {regra}\nnão está no conjunto de estados possíveis do automato {estados}\nAPRESENTE UM ARQUIVO VÁLIDO")
            return False
        if regra_estado_saida not in estados:
            print(f"\nEstado {regra_estado_saida} da regra {regra}\nnão está no conjunto de estados possíveis do automato {estados}\nAPRESENTE UM ARQUIVO VÁLIDO")
            return False
        if regra_letra not in alfabeto:
            print(f"\nSímbolo {regra_letra} da regra {regra}\nnão está no conjunto de símbolos possíveis do automato {alfabeto}\nAPRESENTE UM ARQUIVO VÁLIDO")
            return False
    return True

def main():
    automato = leArquivo()
    dados = limpaPrimeiraLinha(automato)
    estado_inicial = buscaEstadoInicial(automato)
    regras = leRegrasDeTransicao(automato)
    alfabeto = dados[0]
    estados = dados[1]
    estados_finais = dados[2]

    print(f"\n-> Alfabeto: {alfabeto}")
    print(f"-> Estados: {estados}")
    print(f"-> Estado Inicial: {estado_inicial}")
    print(f"-> Estado Final: {estados_finais}")
    print("-> Regras de Transição: ")
    for regra in regras:
        print(regra)
    print()

    if automatoValido(alfabeto, estados, estados_finais, regras):
        print("Processamento: ")
        validade = leituraDaPalavra(estado_inicial, estados_finais, regras)
        if validade:
            print("\nPalavra Válida")
        else:
            print("\nPalavra Inválida")
    else:
        print("\nErro: Autômato inválido.")

if len(sys.argv) != 3:
    print("Requer um arquivo txt e uma palavra para processar")
    print("Tente: python3 main.py <arquivo-txt> <palavra>")
else:
    main()
