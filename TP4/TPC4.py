# Definir o Menu
def Menu():
    print("----------------- MENU -----------------")
    print("(1) Criar Lista")
    print("(2) Ler Lista")
    print("(3) Soma")
    print("(4) Média")
    print("(5) Maior")
    print("(6) Menor")
    print("(7) Está ordenada por ordem crescente")
    print("(8) Está ordenada por ordem decrescente")
    print("(9) Procura um elemento")
    print("(10) Sair")
    print("----------------------------------------")

# Definir as funções
def Criar_Lista():
    import random
    N = int(input("Quantos números deseja que tenha a sua lista?"))
    lista = []
    i = 0
    while i < N:
        x = random.randint(1,100)
        lista.append(x)
        i = i + 1
    return lista


def Ler_Lista():
    lista = []
    entrada = input("Introduza um número da sua lista. Quando não desejar introduzir mais números, escreva <<fim>>.")
    while entrada != "fim":
        x = int(entrada)
        lista.append(x)
        entrada = input("Introduza um número da sua lista. Quando não desejar introduzir mais números, escreva <<fim>>.")
    return lista


def Soma_Lista(lista):
    soma = 0
    i = 0
    while i < len(lista):
        soma = soma + lista[i]
        i = i + 1
    return soma


def Media_Lista(lista):
    soma = Soma_Lista(lista)
    media = 0
    if len(lista) != 0:
        media = soma/len (lista)
    return media


def Maior_Lista(lista):
    maior = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] > maior:
            maior = lista [i]
        i = i + 1
    return maior


def Menor_Lista(lista):
    menor = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] < menor:
            menor = lista [i]
        i = i + 1
    return menor


def Esta_Ordenada_Por_Ordem_Crescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] > lista [i+1]:
            return "Não"
    return "Sim"


def Esta_Ordenada_Por_Ordem_Decrescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] < lista [i+1]:
            return "Não"
    return "Sim"


def Procurar_Elemento(lista):
    x = int(input("Que elemento deseja encontrar na lista?"))
    if x in (lista):
        return f"Elemento encontrado na posição {lista.index(x)}."
    else: 
        return "-1: Elemento não encontrado"

#Definir o Main
def Main():
    lista = []
    cond = True
    while cond:
        Menu()
        opção = input("Introduza a opção pretendida.")

        if opção == "1":
            lista = Criar_Lista()
            print(lista)
            
        elif opção == "2":
            lista = Ler_Lista()
            print(lista)
            
        elif opção == "3":
            res = Soma_Lista(lista)
            print(res)
            
        elif opção == "4":
            res = Media_Lista(lista)
            print(res)
            
        elif opção == "5":
            res = Maior_Lista(lista)
            print(res)
            
        elif opção == "6":
            res = Menor_Lista(lista)
            print(res)
            
        elif opção == "7":
            res = Esta_Ordenada_Por_Ordem_Crescente(lista)
            print(res)
            
        elif opção == "8":
            res = Esta_Ordenada_Por_Ordem_Decrescente(lista)
            print(res)
            
        elif opção == "9":
            res = Procurar_Elemento(lista)
            print(res)
            
        elif opção == "10":
            cond = False
            print("Até à próxima!")
        
        else:
            print("Resposta inválida. Por favor, insira um número entre 1 e 10.")

Main()
