# TPC8

# Parte 1: Especifique as seguintes listas em compreensão: -------------------------------------------------------------------------------------

# Lista formada pelos elementos que não são comuns às duas listas:
lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]
nao_comuns = [x for x in lista1 if x not in lista2] + [x for x in lista2 if x not in lista1] # lista A + lista B = 1 lista com os elementos das listas A e B
print (nao_comuns)


# Lista formada pelas palavras do texto compostas por mais de 3 letras:
texto = """Vivia há já não poucos anos algures num concelho do Ribatejo 
    um pequeno lavrador e negociante de gado chamado Manuel Peres Vigário"""
lista = [x for x in texto.split(" ") if len(x) > 3] 
print(lista)

# for x in texto.split(" ") --> para cada elemento resultante do split da string (texto) pelo caracter " " (espaço)
# if len(x) > 3 --> se o comprimento desse elemento > 3
#   print(x)


# Lista formada por pares do tipo (índice, valor) com os valores da lista dada:
lista = ['anaconda', 'burro', 'cavalo', 'macaco']
listaRes = [(i,lista[i]) for i in range(len(lista))]
print (listaRes)

# for i in range(len(lista)) --> para cada índice desde 0 até (len(lista) - 1)
# print (i, lista[i]) --> print (índice, elemento da lista correspondente a esse índice)


# Parte 2: À semelhança do que foi feito nas aulas, realize as seguintes tarefas: ---------------------------------------------------------------

# Especifique uma função que dada uma string e uma substring não vazia, calcula  o número de vezes em que a substring aparece na string, sem que haja sobreposição de substrings:
def strCount_iterativa(s, subs):
    i = 0
    vezes = 0
    while i < len(s):
        if s[i:i + len(subs)] == subs:
            vezes = vezes + 1
            i = i + len(subs)
        else: i = i + 1
    return vezes

def strCount_recursiva(s, subs):

    if s == "": # caso de paragem
          return 0
    
    if s[0: len(subs)] == subs: # 1º caso a analisar (1º elemento de s)
            return 1 + strCount_recursiva(s[len(subs):], subs) # adicionar 1 à variável de contagem e fazer o mesmo para as restantes posições
    
    else: return strCount_recursiva(s[len(subs):], subs) # a variável de contagem fica igual e fazemos o mesmo para as restantes posições


# Especifique uma função que recebe uma lista de números inteiros positivos e devolve o menor produto que for possível calcular multiplicando os 3 menores inteiros da lista:
def produtoM3(lista):
    lista_ordenada = sorted(lista)
    produto3menores = lista_ordenada[0] * lista_ordenada[1] * lista_ordenada[2]
    return produto3menores


# Especifique uma função que dado um número inteiro positivo, repetidamente adiciona os seus dígitos até obter apenas um dígito que é retornado como resultado:
def reduxInt_iterativa(n):
    while n >= 10: 
        soma = 0
        for digito in str(n):
            soma = soma + int(digito)
        n = soma # atualiza a variável n para a soma dos últimos 2 dígitos
    return n # retorna n se o número tiver apenas 1 dígito


# Especifique uma função que recebe duas strings, `string1` e `string2`, e devolve o índice da primeira ocorrência de `string2` em `string1`, caso não ocorra nenhuma vez a função deverá retornar `-1`:
def myIndexOf_iterativa(s1, s2):
    indice = -1
    i = 0
    while i < len(s1) - len(s2) and indice == -1:
        if s1[i:i + len(s2)] == s2:
            indice = i
        i = i + 1    
    return indice

# -----------

def myIndexOf_recursiva_aux(s1, s2, i):
    if s1 == "" or i > len(s1) - len(s2): 
        return "-1"
    
    if s1[i:i + len(s2)] == s2:
        return i
    
    else:
        return myIndexOf_recursiva_aux(s1, s2, i + 1)


def myIndexOf_recursiva(s1, s2):
    return myIndexOf_recursiva_aux(s1, s2, 0)


# Parte 3: A Rede Social -----------------------------------------------------------------------------------------------------------------------

# Rede social = lista de dicionários
# Dicionário (=post) tem chaves 'id', 'conteudo', 'autor', 'dataCriacao' e 'comentarios'
# 'comentarios' = lista de dicionários com chaves 'comentario' e 'autor'

# Exemplo::
# MyFaceBook = [{'id': 'p1', 'conteudo': 'A tarefa de avaliação é talvez a mais ingrata das tarefas que um professor tem de realizar...','autor': 'jcr',
# 'dataCriacao': '2023-07-20', 'comentarios': [{'comentario': 'Completamente de acordo...', 'autor': 'prh'}, {'comentario': 'Mas há quem goste...', 'autor': 'jj'}]}

# Definir as Funções

# Indica quantos posts estão registados:
def quantosPost(redeSocial):
    return len(redeSocial)

# Devolve a lista de posts de um determinado autor:
def postsAutor(redeSocial, autor):
    posts_autor = []
    for post in redeSocial:
        if post["autor"] == autor:
            posts_autor.append(post)
    return posts_autor

# Devolve a lista de autores de posts ordenada alfabeticamente:
def autores(redeSocial):
    lista_autores = [post["autor"] for post in redeSocial]
    lista_autores_ordenada = sorted(lista_autores)
    return lista_autores_ordenada

# Acrescenta um novo post à rede social a partir dos parâmetros recebidos e devolve a nova rede social:
# O campo `id` deverá ser calculado a partir dos já existentes, por exemplo, se a rede tiver posts com id `p1`, `p2` e `p3`, o novo `id` deverá ser `p4`.
def insPost(redeSocial, conteudo, autor, dataCriacao, comentarios):
    if redeSocial == []:
        novo_id = "p1"
    else: novo_id = f"p{len(redeSocial) + 1}"
    novo_post = {'id': novo_id, 'conteudo': conteudo, 'autor': autor, 'dataCriacao': dataCriacao, 'comentarios': comentarios}
    redeSocial.append(novo_post)
    return redeSocial

# Remove um post da rede, correspondente ao `id` recebido:
def remPost(redeSocial, id):
    for post in redeSocial:
        if post["id"] == id:
            redeSocial.remove(post)
    return redeSocial

# Devolve uma distribuição de posts por autor (à semelhança do que foi feito nas aulas):
def postsPorAutor(redeSocial):
    dicionario = {} # começamos com dicionário (distribuição) vazio
    for post in redeSocial:
        autor = post["autor"] # para cada post, o seu autor será uma chave no novo dicionário
        if autor not in dicionario:
            dicionario[autor] = 1
        else:
            dicionario[autor] = dicionario[autor] + 1
    return dicionario

# Recebe um autor e devolve a lista de posts comentados por esse autor:
def comentadoPor(redeSocial, autor):
    postsComentadosAutor = []
    for post in redeSocial:
        for comentario in post["comentarios"]:
            if comentario["autor"] == autor:
                postsComentadosAutor.append(post)
    return postsComentadosAutor
