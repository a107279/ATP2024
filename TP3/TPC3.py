import random
def fosforos(fosforos_restantes):
    jogador= input("Se quiser jogar primeiro pressione 'H',caso queira que comece o computador pressione 'C': ")
    if(jogador=="h" or jogador=="H"):
        while(fosforos_restantes>=1):
            fosforos_h= int(input("Quantos fósforos quer tirar?"))
            if(fosforos_h<1 or fosforos_h>4):
                print("Não pode retirar mais de 4 fósforos de cada vez ou menos do que 1!")
                break
            fosforos_restantes=fosforos_restantes-fosforos_h
            print("Restam",fosforos_restantes,"fósforos")
            fosforos_c= 5-fosforos_h
            fosforos_restantes=fosforos_restantes-fosforos_c
            print("O computador retirou",fosforos_c,"e sobram",fosforos_restantes,"fósforos")

            if(fosforos_restantes==1):
                print("Você perdeu!")
                break
    elif (jogador=="c" or jogador=="C"):
        while(fosforos_restantes>=1):
            if(fosforos_restantes==2 or fosforos_restantes==3 or fosforos_restantes==4 or fosforos_restantes==5):
                fosforos_c=fosforos_restantes-1
                print("O computador retirou",fosforos_c)
                print("Você perdeu!")
                break
            elif(fosforos_restantes==1):
                print("Você ganhou!")
                break
            fosforos_c= random.randint(1,4)
            fosforos_restantes=fosforos_restantes-fosforos_c
            print("O computador retirou",fosforos_c,"e sobraram",fosforos_restantes,"fósforos!")
            fosforos_h=int(input("Quantos fósforos quer tirar?"))
            if(fosforos_h<1 or fosforos_h>4):
                print("Não pode retirar mais de 4 fósforos de cada vez ou menos do que 1!")
                break
            fosforos_restantes=fosforos_restantes-fosforos_h
            print("Restam",fosforos_restantes,"fósforos")
fosforos(21)