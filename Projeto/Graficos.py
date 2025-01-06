import FreeSimpleGUI as sg
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime


def exibir_menu_relatorios(publicacoes):
    sg.theme("DarkTeal4")
    layout_relatorios = [
        [sg.Text("Escolha um Relatório para Gerar", font=("Arial", 14), justification="center")],
        [sg.Button("Distribuição de Publicações por Ano", key="-REL_ANO-")],
        [sg.Button("Distribuição de Publicações por Mês de um Ano", key="-REL_MES_ANO-")],
        [sg.Button("Número de Publicações por Autor (Top 20)", key="-REL_AUTOR-")],
        [sg.Button("Distribuição de Publicações por Autor por Ano", key="-REL_AUTOR_ANO-")],
        [sg.Button("Distribuição de Palavras-chave por Frequência", key="-REL_PALAVRAS-")],
        [sg.Button("Distribuição de Palavras-chave por Ano", key="-REL_PALAVRAS_ANO-")],
        [sg.Button("Fechar", key="-FECHARREL-")]
    ]
    
    window_relatorios = sg.Window("Relatórios de Estatísticas", layout_relatorios, font=("Arial"), finalize=True)
    
    stop = False
    while not stop:
        event, values = window_relatorios.read()
        
        if event == sg.WINDOW_CLOSED or event == "-FECHARREL-":
            stop = True
            window_relatorios.close()
        elif event == "-REL_ANO-":
            distribucao_por_ano(publicacoes)  # Chama a função que gera o gráfico de publicações por ano
        elif event == "-REL_MES_ANO-":
            ano_especifico = sg.popup_get_text("Digite o ano:", title="Ano específico")
            if ano_especifico:
                distribucao_por_mes_ano(publicacoes, int(ano_especifico))
        elif event == "-REL_AUTOR-":
            publicacoes_por_autor(publicacoes)
        elif event == "-REL_AUTOR_ANO-":
            autor = sg.popup_get_text("Digite o nome do autor:", title="Autor")
            if autor:
                publicacoes_por_ano_autor(publicacoes, autor)
        elif event == "-REL_PALAVRAS-":
            palavras_chave_frequencia(publicacoes)
        elif event == "-REL_PALAVRAS_ANO-":
            palavras_chave_por_ano(publicacoes)


# ESTATISTICAS DE PUBLICAÇÃO (GRÁFICOS)
def distribucao_por_ano(dataset):
    anos = []
    for pub in dataset:
        if 'publish_date' in pub and pub['publish_date']:
            # Limpa a string de data, removendo qualquer texto adiconal
            data_pub = pub['publish_date'].split(" —")[0]  # pegar só na parte da data
            
            if len(data_pub) == 10:     # Verificar se a data tem o formato correto "YYYY-MM-DD"
                try:
                    ano = datetime.strptime(data_pub, "%Y-%m-%d").year
                    anos.append(ano)
                except ValueError:
                    print(f"A data '{data_pub}' não pode ser convertida para o formato esperado.")
            else:
                print(f"A data '{pub['publish_date']}' não tem o formato esperado.")  # Apenas imprime a data inválida
        else:
            print(f"A publicação não tem o campo 'publish_date'.")  # Caso não exista 'publish_date'
    
    if anos:
        contagem_anos = Counter(anos)
    
        plt.figure(figsize=(10, 6))
        plt.bar(contagem_anos.keys(), contagem_anos.values())
        plt.title("Distribuição de Publicações por Ano")
        plt.xlabel("Ano")
        plt.ylabel("Número de Publicações")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Nenhuma publicação com data válida encontrada.")

def distribucao_por_mes_ano(dataset, ano_especifico):
    meses = []
    for pub in dataset:
        if 'publish_date' in pub:     
            data_pub = pub['publish_date'].split(" —")[0]   # Divide a string e pega a parte da data no formato "YYYY-MM-DD"
            
            try:
                # Tenta converter a string de data para o formato datetime
                data = datetime.strptime(data_pub, "%Y-%m-%d")
                
                # Verifica se o ano da data da publicação corresponde ao ano específico fornecido
                if data.year == ano_especifico:
                    # Se sim, adiciona o mês da publicação à lista 'meses'
                    meses.append(data.month)  # Armazena o mês (numérico de 1 a 12)
            except ValueError:
                print(f"A data '{data_pub}' não tem o formato esperado.")
        else:
            print(f"A publicação não tem o campo 'publish_date'. Ignorando...")

    # Verifica se a lista 'meses' está vazia, ou seja, se não foram encontradas publicações para o ano especificado
    if not meses:
        print(f"Não existem publicações para o ano {ano_especifico}.")
        return 
    
    contagem_meses = Counter(meses)   # Contar as ocorrências de cada mês
    
    plt.figure(figsize=(10, 6))
    plt.bar(contagem_meses.keys(), contagem_meses.values())
    plt.title(f"Distribuição de Publicações por Mês de {ano_especifico}")
    plt.xlabel("Mês")
    plt.ylabel("Número de Publicações")
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.tight_layout()
    plt.show()



def publicacoes_por_autor(dataset):
    autores = []
    
    for pub in dataset:
        # Usa .get() para garantir que o acesso a 'authors'
        authors = pub.get('authors', None)

        if authors:
            # Se 'authors' for uma lista de dicionários
            for autor in authors:
                if 'name' in autor:  # Verifica se o campo 'name' está presente
                    autores.append(autor['name'].strip())  # Adiciona o nome do autor à lista
                else:
                    print(f"Autor inválido encontrado (sem nome): {autor}")
        else:
            print(f"Chave 'authors' ausente ou inválida na publicação: {pub}")

    if not autores:  # Verificar se a lista de autores não está vazia
        print("Nenhum autor encontrado nas publicações. Verifique os dados.")
        return  # Sai da função se não houver autores

    contagem_autores = Counter(autores)  # Contagem de autores
    top_autores = contagem_autores.most_common(20)

    # Se top_autores estiver vazio, significa que não houve autores válidos
    if not top_autores:
        print("Nenhum autor encontrado para gerar o gráfico.")
        return

    nomes, contagens = zip(*top_autores)

    plt.figure(figsize=(10, 6))
    plt.barh(nomes, contagens)
    plt.title("Número de Publicações por Autor (Top 20)")
    plt.xlabel("Número de Publicações")
    plt.ylabel("Autor")
    plt.tight_layout()
    plt.show()


def publicacoes_por_ano_autor(dataset, autor):
    anos = []
    sem_data = 0  # Contador para publicações sem data
    autor_normalizado = autor.strip()  # Remover espaços extras´

    # Variável de controle para verificar se o autor tem publicações
    autor_tem_publicacao = False

    for pub in dataset:
        print(f"Verificando publicação: {pub}")  # verificar
        if 'authors' in pub:
            
            autores = [autor['name'].strip() for autor in pub['authors']]   # normalizar os nomes dos autores removendo espaços extras
            
            if autor_normalizado in autores:    # comparação exata do nome (sem ignorar maiúsculas/minúsculas)
                autor_tem_publicacao = True  # Marcar que o autor tem publicações
                if 'publish_date' in pub and pub['publish_date']:  
                    try:
                        ano = datetime.strptime(pub['publish_date'], "%Y-%m-%d").year
                        anos.append(ano)
                    except ValueError:
                        print(f"Data inválida para publicação: {pub['publish_date']}")
                        sem_data = sem_data + 1
                else:
                    sem_data += 1   # ir contando as publicações sem data
        else:
            print(f"Chave 'authors' ausente na publicação: {pub}")

    if not autor_tem_publicacao and sem_data==0:
        print(f"O autor '{autor}' não possui publicações no dataset.")
        return

    contagem_anos = Counter(anos)       # contar frequência dos anos
    anos_ordenados = sorted(contagem_anos.items())  # ordenar os anos
    
    anos_labels = [str(ano) for ano, _ in anos_ordenados]
    anos_values = [count for _, count in anos_ordenados]

    if sem_data > 0:        # se houver pubs sem data
        anos_labels.append("Sem Data")
        anos_values.append(sem_data)

    plt.figure(figsize=(10, 6))
    plt.bar(anos_labels, anos_values, color='skyblue')
    plt.title(f"Distribuição de Publicações de {autor} por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.xticks(rotation=45)
    if max(anos_values) > 0:
        plt.ylim(0, max(anos_values) + 1)  # Ajustar o limite do eixo Y
    else:
        plt.ylim(0, 1)  # Garantir que o gráfico não fique vazio
    plt.tight_layout()
    plt.show()



def palavras_chave_frequencia(dataset):
    palavras_chave = []
    for pub in dataset:
        if 'keywords' in pub:
            keywords = pub['keywords']
            
            # Se 'keywords' é uma string, separa as palavras por vírgula
            palavras_chave.extend(palavra.strip().lower() for palavra in keywords.split(','))

    contagem_palavras_chave = Counter(palavras_chave)   # Contagem das palavras-chave
    
    # Seleciona as 20 palavras-chave mais comuns
    top_palavras = contagem_palavras_chave.most_common(20)
    palavras, frequencias = zip(*top_palavras)
    
    plt.figure(figsize=(10, 6))
    plt.barh(palavras, frequencias)
    plt.title("Distribuição de Palavras-chave por Frequência (Top 20)")
    plt.xlabel("Frequência")
    plt.ylabel("Palavra-chave")
    plt.tight_layout()
    plt.show()



def palavras_chave_por_ano(dataset):
    layout = [
        [sg.Text("Digite o ano para analisar as palavras-chave mais frequentes (formato: YYYY):")],
        [sg.InputText(key="-ANO-")],
        [sg.Button("Confirmar"), sg.Button("Cancelar")]
    ]
    window = sg.Window("Entrada de Ano", layout, font=("Helvetica", 12))
    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            window.close()
            return  # sai da função se cancelar ou fechar a janela
        if event == "Confirmar":
            ano_desejado = values["-ANO-"]
            if ano_desejado.isdigit() and len(ano_desejado) == 4:
                ano_desejado = int(ano_desejado)
                stop = True  # o loop acaba ao inserir um ano válido
            else:
                sg.popup_error("Por favor, insira um ano válido no formato: YYYY.")
    window.close()

    palavras_ano = {}

    for pub in dataset:
        palavras = []
        if 'publish_date' in pub:
            try:
                ano = datetime.strptime(pub['publish_date'], "%Y-%m-%d").year
            except ValueError:
                ano = None  # Ignorar se a data não for válida
        else:
            ano = None  # Ignorar se a chave 'publish_date' não existir

        # Se o ano da publicação for igual ao ano sselecionado, processa as palavras-chave
        if ano == ano_desejado and ano is not None:
            if 'keywords' in pub and pub['keywords']:  # Apenas verifica se existe e não é vazio
                keywords = pub['keywords'].split(",")  # Divide diretamente
                palavras.extend([palavra.strip().lower() for palavra in keywords])

        for palavra in palavras:
            if palavra:
                if palavra in palavras_ano:
                    palavras_ano[palavra] += 1
                else:
                    palavras_ano[palavra] = 1

    if not palavras_ano:        # Se não houver palavras-chave para o ano selecionado
        sg.popup_error(f"Não há dados disponíveis (palavras-chave ou ano) para o ano {ano_desejado}.")
        return

    # Ordenar as palavras por frequência e selecionar as mais frequentes, escolhemos mostrar as 10 mais frequentes
    top_palavras = sorted(palavras_ano.items(), key=lambda x: x[1], reverse=True)[:10]
    palavras, frequencias = zip(*top_palavras)

    plt.figure(figsize=(10, 6))
    plt.barh(palavras, frequencias)
    plt.title(f"Distribuição de Palavras-chave mais Frequentes em {ano_desejado}")
    plt.xlabel("Frequência")
    plt.ylabel("Palavra-chave")
    plt.tight_layout()
    plt.show()