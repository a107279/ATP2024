def existe(cinema, filme):
    cond = False
    for sala in cinema:
        if sala[2] == filme:        
            cond = True
    return cond

def inserirSala(cinema, sala):
    if not existe(cinema, sala[2]):
        cinema.append(sala)
        print("A sala foi adicionada!")
    else:
        print(f"A sala com o filme {sala[2]} já existe.")
    return cinema

def listar(cinema):
    print ("-----------------Lista de Filmes---------------")
    for sala in cinema:
        nlugares, vendidos, nomef = sala                           
        print(f"Filme: {nomef}       | Nº Lugares: {nlugares}")
    print("------------------------------------------------")
    return

def disponivel(cinema, filme, lugar):
    cond = False
    for sala in cinema:
        nlugares, vendidos, nomef = sala
        if nomef == filme and lugar <= nlugares and lugar not in vendidos:
                cond = True
    return cond 

def vendeBilhete(cinema, filme, lugar):     
    if disponivel(cinema, filme, lugar):
        for sala in cinema:
            nlugares, vendidos, nomef = sala
            if nomef == filme:
                vendidos.append(lugar)
                return f"O lugar {lugar} para o filme {filme} foi adquirido com sucesso!"
    return f"O lugar {lugar} para o filme {filme} não está disponível. Selecione outra opção."
        

def listardisponibilidades( cinema ):
    print("----------------Disponibilidade do Cinema----------------")
    for sala in cinema:
        nlugares, vendidos, nomef = sala
        disponiveis = nlugares - len(vendidos)      
        print (f"Nome: {nomef}      | Lugares Disponíveis: {disponiveis}")
    print("----------------------------------------------------------")
    return

sala1 = (150, [], "Twilight")
sala2 = (200, [13, 48, 49, 175], "Hannibal")

cinema =[sala1, sala2]

def menu(cinema):

    cond = True
    opcoes = ("1" , "2" , "3" , "4" , "5") 
    while cond:
        print("---------------Gestão de Salas de Cinema---------------\n 1 - Listar todos os filmes\n 2 - Listar a disponibilidade das salas dos filmes\n 3 - Vender bilhetes para um filme\n 4 - Adiciona uma nova sala de cinema\n 5 - Sair")

        escolha = input("Escolha a sua opção introduzindo um número da lista:")

        if escolha in opcoes:

            if escolha == "1":
                listar(cinema)
            
            if escolha == "2":
                listardisponibilidades(cinema)
            
            if escolha == "3":
                filme = str(input("Introduz o nome do filme que deseja ver:"))
                lugar = int(input(f"Introduza o número do lugar, entre 1 e o nº de lugares da sala, para o filme {filme}:"))
                res = vendeBilhete(cinema, filme, lugar)
                print(res)

            if escolha == "4":
                filme = str(input("Introduza o nome do filme:"))
                nlugares = int(input(f"Introduza o número de lugares da sala do filme {filme}:"))
                novoFilme = [nlugares, [], filme]   
                cinema = inserirSala( cinema, novoFilme )
            
            if escolha == "5":
                print("Escolheu a opção de sair. Até à próxima!")
                cond = False
        else:
            print("Opção inválida. Por favor, escolha outra opção.")
menu(cinema)