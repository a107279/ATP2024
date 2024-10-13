def jogo_adivinha_numero():
    print("Bem vindo ao jogo Adivinha o Número!")
    print("Escolha uma modalidade:")
    print("1. O computador pensa num número e você tenta adivinhar.")
    print("2. Você pensa num número e o computador tenta adivinhar.")
    
    modalidade = input("Digite 1 ou 2: ")

    if modalidade == "1":
        # Computador pensa num número
        import random
        numero = random.randint(0, 100)
        tentativas = 0
        acertou = False

        print("O computador pensou num número entre 0 e 100. Tente adivinhar!")

        while not acertou:
            palpite = int(input("Digite seu palpite: "))
            tentativas = tentativas + 1

            if palpite == numero:
                print("Acertou! O número era:", numero)
                acertou = True
            elif palpite < numero:
                print("O número que pensei é Maior.")
            else:
                print("O número que pensei é Menor.")

        print(f"Você precisou de {tentativas} tentativas para acertar.")

    elif modalidade == "2":
        # Utilizador pensa num número
        print("Pense num número entre 0 e 100 e o computador vai tentar adivinhar")

        minimo, maximo = 0, 100
        tentativas = 0
        acertou = False

        while not acertou:
            palpite = (minimo + maximo) // 2
            tentativas = tentativas + 1
            print("Meu palpite é:", palpite)
            resposta = input("Digite 'Acertou', 'Maior' ou 'Menor': ")

            if resposta == "Acertou":
                print("Eu acertei! O número era:", palpite)
                acertou = True
            elif resposta == "Maior":
                minimo = palpite + 1
            elif resposta == "Menor":
                maximo = palpite - 1

        print(f"Eu precisei de {tentativas} tentativas para acertar.")

    else:
        print("Modalidade inválida! Por favor, escolha 1 ou 2.")

# Inicia o jogo
jogo_adivinha_numero()
