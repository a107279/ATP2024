def mostrar_menu():
    print("----------Menu de Operações----------")
    print("1: Criar uma turma")
    print("2: Inserir um aluno na turma")
    print("3: Listar a turma")
    print("4: Consultar um aluno por ID")
    print("5: Guardar a turma em ficheiro")
    print("6: Carregar uma turma de um ficheiro")
    print("0: Sair da aplicação")
    print("-------------------------------------")


def criar_turma():
    return []


def inserir_aluno(turma):
    nome = input("Nome do aluno: ")
    id = input("ID do aluno: ")
    notaTPC = float(input("Nota TPC: "))
    notaProj = float(input("Nota Projeto: "))
    notaTeste = float(input("Nota Teste: "))
    aluno = (nome, id, [notaTPC, notaProj, notaTeste])
    turma.append(aluno)
    print(f"\nAluno {nome} inserido com sucesso!")
    return turma


def listar_turma(turma):
    if turma:
        print("\nListagem da turma:")
        for aluno in turma:
            print(f"Nome: {aluno[0]}, ID: {aluno[1]}, Notas: TPC: {aluno[2][0]}, Projeto: {aluno[2][1]}, Teste: {aluno[2][2]}")
    else:
        print("\nA turma está vazia.")

# Função para consultar um aluno por ID
def consultar_aluno_por_id(turma):
    id_consulta = input("Digite o ID do aluno que deseja consultar: ")
    aluno_encontrado = next((aluno for aluno in turma if aluno[1] == id_consulta), None)
    if aluno_encontrado:
        print(f"\nAluno encontrado! Nome: {aluno_encontrado[0]}, Notas: TPC: {aluno_encontrado[2][0]}, Projeto: {aluno_encontrado[2][1]}, Teste: {aluno_encontrado[2][2]}")
    else:
        print("\nAluno não encontrado.")

# Função para guardar a turma em ficheiro
def guardar_turma_em_ficheiro(turma):
    nome_ficheiro = input("Nome do ficheiro para guardar (ex: turma.txt): ")
    try:
        with open(nome_ficheiro, 'w') as ficheiro:
            for aluno in turma:
                linha = f"{aluno[0]},{aluno[1]},{aluno[2][0]},{aluno[2][1]},{aluno[2][2]}\n"
                ficheiro.write(linha)
        print(f"\nTurma guardada com sucesso no ficheiro {nome_ficheiro}!")
    except Exception as e:
        print(f"\nErro ao guardar a turma: {e}")

# Função para carregar a turma de um ficheiro
def carregar_turma_de_ficheiro():
    nome_ficheiro = input("Nome do ficheiro para carregar (ex: turma.txt): ")
    try:
        turma = []
        with open(nome_ficheiro, 'r') as ficheiro:
            for linha in ficheiro:
                dados = linha.strip().split(",")
                nome = dados[0]
                id = dados[1]
                notas = [float(dados[2]), float(dados[3]), float(dados[4])]
                aluno = (nome, id, notas)
                turma.append(aluno)
        print(f"\nTurma carregada com sucesso do ficheiro {nome_ficheiro}!")
        return turma
    except Exception as e:
        print(f"\nErro ao carregar a turma: {e}")
        return []

# Função principal para controlar o menu e fluxo do programa
def main():
    turma = []  # A turma começa vazia
    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ")
        if opcao == "1":
            turma = criar_turma()
            print("\nNova turma criada.")
        elif opcao == "2":
            turma = inserir_aluno(turma)
        elif opcao == "3":
            listar_turma(turma)
        elif opcao == "4":
            consultar_aluno_por_id(turma)
        elif opcao == "5":
            guardar_turma_em_ficheiro(turma)
        elif opcao == "6":
            turma = carregar_turma_de_ficheiro()
        elif opcao == "0":
            print("\nSaindo da aplicação...")

if __name__ == "__main__":
    main()
