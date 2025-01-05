import json
import FreeSimpleGUI as sg
from datetime import datetime

res_pesquisa ={}

def print_help():
    sg.theme("DarkRed")
    help_text = """
    Comandos disponíveis:
    - Criar Publicação: Criar uma nova publicação.
    - Consulta de Publicação: Consultar uma publicação através do seu DOI.
    - Consulta de Publicação Por: Pesquisa de publicação/ões através de filtros: título, autor, palavra-chave, data de publicação, afiliação.
    - Atualizar Publicações: Atualizar campo/s de uma publicação.
    - Eliminar Publicação: Eliminar uma publicação.
    - Relatório de Estatísticas: Gerar relatórios sobre as publicações.
    - Listar Autores: Listar todos os autores e as suas publicações associadas.
    - Listar Palavras-Chave: Listar todas as palavras-chave e as suas publicações associadas.
    - Importar Publicações: Importar publicações de um arquivo.
    - Guardar publicações: Guardar as publicações para um arquivo.
    - Exportar Última Pesquisa: Guardar num ficheiro JSON a última pesquisa/consulta realizada.
    
    """
    sg.popup(help_text, title="Ajuda")


# Função para carregar o arquivo JSON e retornar os dados
def carregaDados(fnome):
    res = []
    try:
        with open(fnome, encoding='utf-8') as f:
            conteudo = f.read()  # Lê o conteúdo do arquivo
        
        res = json.loads(conteudo)  # Tenta carregar o conteúdo como JSON
    
    except json.JSONDecodeError:
        sg.popup_error("Erro: O conteúdo do arquivo não é um JSON válido.")  #  mensagem de erro
        return []  # Retorna uma lista vazia, evita que a aplicação continue com dados inválidos
    return res

def procuraFicheiro():
    print("Procurando...")
    layout = [
        [sg.Button("Procurar ficheiro", key='-PROCURAR-')],
        [sg.Text("Nenhum ficheiro selecionado.", key='-RESULTADO-', size=(30, 1))]
    ]

    window = sg.Window("Procurar ficheiro", layout, font=("Helvetica", 15))

    file=""
    stop=False
    while not stop:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            stop=True
        elif event == '-PROCURAR-':
            file = sg.popup_get_file('Procurar ficheiro', no_window=True, font=("Helvetica", 15))
            if file:
                window['-RESULTADO-'].update(f"ficheiro selecionado: {file}")
                window.close()
            else:
                window['-RESULTADO-'].update("Nenhum ficheiro selecionado.")

    window.close()
    if file=="":
        file=None
    return file


# Função para salvar os dados no arquivo JSON
def salvaDados(dataset):

    layout = [[sg.Text("Introduza o nome do ficheiro no qual deseja guardar os dados:")],
            [sg.Text("Nome", size=(11,2)), sg.InputText(key="-FNOME-"), sg.Text('.json', size=(6,2))],
            [sg.Button("Inserir", key="-INSERIR-"), sg.Button("Cancelar", key="-CANCELAR-")]]

    windowLayout = sg.Window("Guardar Dados", layout, location = (200, 300), font = ("Helvetica", 16))

    stop = False
    while not stop:
        event, values = windowLayout.read() 
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-INSERIR-":
            fnome = values['-FNOME-'].strip()
            if not fnome.endswith('.json'):        # verificar se o usuário escreveu com '.json' porque se caso escreveu, não acrescentar novamente
                fnome = fnome + '.json'
            # Abrir o arquivo para escrever os dados
            f = open(fnome, 'w', encoding='utf-8')
            json.dump(dataset, f, ensure_ascii=False, indent=4)
            f.close()
            sg.popup("Sucesso!", f"Dados salvos com sucesso em {fnome}") 
            stop = True
        
    windowLayout.close()
    return event, values


def criar_publicacao(dataset, fnome):
    # Abrir o arquivo e carregar o dataset existente
    fIn = open(fnome, "r", encoding='utf-8')
    publicacoes = json.load(fIn)
    fIn.close()

    sg.theme("DarkGreen5")

    layout = [
        [sg.Text("Título:"), sg.InputText(do_not_clear=True, key="-TITULO-")],
        [sg.Text("Resumo:"), sg.InputText(do_not_clear=True, key="-RESUMO-")],
        [sg.Text("Palavras-Chave (separadas por vírgulas):"), sg.InputText(do_not_clear=True, key="-KEYWORDS-")],
        [sg.Text("DOI:"), sg.InputText(do_not_clear=True, key="-DOI-")],
        [sg.Text("URL do PDF:"), sg.InputText(do_not_clear=True, key="-PDF-")],
        [sg.Text("Data de Publicação:"), sg.InputText(key="-DATA-", readonly=True), sg.CalendarButton("Escolher Data", target="-DATA-", format="%Y-%m-%d")],
        [sg.Text("URL do Artigo:"), sg.InputText(do_not_clear=True, key="-URL-")],
        [sg.Text("Autores (adicione o nome e a afiliação):")],
        [sg.Text("Nome do Autor:"), sg.InputText(do_not_clear=True, key="-AUTOR-"),
         sg.Text("Afiliação:"), sg.InputText(do_not_clear=True, key="-AFILIACAO-")],
        [sg.Button("Adicionar autor à lista:", key="-ADD_AUTOR-"), sg.Button("Guardar Publicação", key="-GUARDAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        [sg.Listbox(values=[], key="-LISTA_DE_AUTORES-", size=(40, 10))]
    ]
    
    windowCriar = sg.Window("Criar nova publicação", layout, location=(100, 100), font=("Helvetica", 16))

    autores = []  # Lista para armazenar os autores
    stop = False
    while not stop:
        event, values = windowCriar.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        
        if event == "-ADD_AUTOR-":
            author_name = values["-AUTOR-"].strip()
            affiliation = values["-AFILIACAO-"].strip()

            if author_name:
                autor = {"name": author_name.strip()}
                if affiliation:  # Só adicionar 'affiliation' se houver um valor
                    autor["affiliation"] = affiliation.strip()
                autores.append(autor)

        # Atualizar a lista de autores exibida na interface
                windowCriar["-LISTA_DE_AUTORES-"].update([
                    f"{autor['name']} ({autor.get('affiliation', 'Sem afiliação')})" for autor in autores
                ])
                windowCriar["-AUTOR-"].update("")
                windowCriar["-AFILIACAO-"].update("")
            else:
                sg.popup_error("Erro! O campo Nome do Autor é obrigatório.")

        if event == "-GUARDAR-":
            # Validação para garantir que o DOI seja único
            doi = values["-DOI-"].strip()
            if not doi:
                sg.popup_error("Erro! O campo DOI é obrigatório!")
            elif any(pub.get("doi") == doi for pub in dataset):
                sg.popup_error("Erro: Já existe uma publicação com este DOI.")
            else:
                # Criar um dicionário para a nova publicação
                nova_publicacao = {}
                
                # Adicionar campos preenchidos à nova publicação
                if values["-RESUMO-"].strip():
                    nova_publicacao["abstract"] = values["-RESUMO-"].strip()
                if values["-KEYWORDS-"].strip():
                    nova_publicacao["keywords"] = ", ".join([kw.strip() for kw in values["-KEYWORDS-"].split(",") if kw.strip()]) 
                if autores:
                    nova_publicacao["authors"] = autores   
                if values["-DOI-"].strip():
                    nova_publicacao["doi"] = values["-DOI-"].strip()  
                if values["-PDF-"].strip():
                    nova_publicacao["pdf"] = values["-PDF-"].strip()    
                if values["-DATA-"].strip():
                    nova_publicacao["publish_date"] = values["-DATA-"].strip()
                if values["-TITULO-"].strip():
                    nova_publicacao["title"] = values["-TITULO-"].strip()
                if values["-URL-"].strip():
                    nova_publicacao["url"] = values["-URL-"].strip()

                # Adicionar a nova publicação ao dataset
                dataset.append(nova_publicacao)
                sg.popup("Publicação criada com sucesso!")
                stop = True

    windowCriar.close()

    # Salvar o dataset atualizado no arquivo
    fOut = open(fnome, "w", encoding='utf-8')
    json.dump(dataset, fOut, ensure_ascii=False, indent=4)
    fOut.close()

    return dataset



def atualizar_publicacao(dataset, fnome):
    
    # Abrir o arquivo e carregar o dataset existente
    fIn = open(fnome, "r", encoding='utf-8')
    publicacoes = json.load(fIn)
    fIn.close()
    
    doi_layout = [
        [sg.Text("Insira o DOI da publicação que deseja atualizar:")],
        [sg.InputText(key="-DOI-", size=(50, 1))],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    doi_window = sg.Window("Selecionar Publicação por DOI", doi_layout, font=("Helvetica", 15))

    selected_pub = None
    stop = False
    while not stop:
        event, values = doi_window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
            doi_window.close()
            return dataset 

        elif event == "-CONFIRMAR-":
            doi_input = values["-DOI-"].strip()
            if not doi_input:
                sg.popup("Por favor, insira um DOI válido.", font=("Helvetica", 15))
            else:
                for pub in dataset:     # Verificar se o DOI está no dataset
                    if pub.get("doi") == doi_input:
                        selected_pub = pub
    
                if selected_pub:
                    sg.popup(f"Publicação encontrada!", font=("Helvetica", 15))
                    stop = True  
                else:
                    sg.popup("DOI não encontrado no dataset. Tente novamente.", font=("Helvetica", 15))

    doi_window.close()

    parametro_stop = False
    while not parametro_stop:
        parametro_layout = [
            [sg.Text("Selecione o parâmetro para atualizar:")],
            [sg.Combo(["Título", "Data de Publicação", "Resumo", "Palavras-Chave", "Autores", "Afiliações"], key="-PARAMETRO-", size=(30, 1))],
            [sg.Button("Atualizar", key="-ATUALIZAR-"), sg.Button("Finalizar Atualizações", key="-FINALIZAR-")]
        ]
        parametro_window = sg.Window("Selecionar Parâmetro", parametro_layout, font=("Helvetica", 15))

        event, values = parametro_window.read()
        if event in (sg.WINDOW_CLOSED, "-FINALIZAR-"):
            parametro_stop = True
        elif event == "-ATUALIZAR-":
            parametro = values["-PARAMETRO-"]
            if not parametro:
                sg.popup("Por favor, selecione um parâmetro para atualizar.", font=("Helvetica", 15))
            else:
                if parametro == "Título":
                    novo_titulo = sg.popup_get_text("Insira o novo título da publicação:", font=("Helvetica", 15))
                    if novo_titulo:
                        selected_pub["title"] = novo_titulo  

                elif parametro == "Data de Publicação":
                    data_stop = False
                    while not data_stop:
                        nova_data = sg.popup_get_text("Insira a nova data de publicação (YYYY-MM-DD):", font=("Helvetica", 15))
                        if nova_data: 
                            # Verificar se a data está no formato correto :
                            if len(nova_data) == 10 and nova_data[4] == '-' and nova_data[7] == '-' and nova_data[:4].isdigit() and nova_data[5:7].isdigit() and nova_data[8:].isdigit():
                                selected_pub["publish_date"] = nova_data
                                data_stop = True  # data válida --> interrompe o loop
                            else:
                                sg.popup_error("Data inválida! Use o formato YYYY-MM-DD.", font=("Helvetica", 15))
                        else:
                            data_stop = True  # campo vazio --> não atualiza e sai

                elif parametro == "Resumo":
                    novo_resumo = sg.popup_get_text("Insira o novo resumo:", font=("Helvetica", 15))
                    if novo_resumo:
                        selected_pub["abstract"] = novo_resumo

                elif parametro == "Palavras-Chave":
                    nova_palavra = sg.popup_get_text("Insira as nova(s) palavras-chave (separadas por vírgulas):", font=("Helvetica", 15))
                    if nova_palavra:
                        selected_pub["keywords"] = ", ".join([kw.strip() for kw in nova_palavra.split(",")])

                elif parametro == "Autores":
                    novos_autores = sg.popup_get_text("Insira os novos autores (separados por vírgulas):", font=("Helvetica", 15))
                    if novos_autores:
                        novos_nomes = [nome.strip() for nome in novos_autores.split(",")]

                        # Atualizar mantendo as afiliações e outros campos dos autores existentes
                        for i, nome in enumerate(novos_nomes):
                            if i < len(selected_pub["authors"]):
                                selected_pub["authors"][i]["name"] = nome  # Atualizar nome
                            else:
                                # Adicionar novos autores, caso a lista de novos seja maior
                                selected_pub["authors"].append({
                                    "name": nome,
                                    "affiliation": "Sem afiliação",
                                })

                elif parametro == "Afiliações":
                    novas_afiliacoes = sg.popup_get_text("Insira as novas afiliações (separadas por vírgulas):", font=("Helvetica", 15))
                    if novas_afiliacoes:
                        lista_afiliacoes = [afiliacao.strip() for afiliacao in novas_afiliacoes.split(",")]

        # Garantir que o número de afiliações não exceda o número de autores
                        if len(lista_afiliacoes) > len(selected_pub["authors"]):
                            sg.popup("Erro: O número de afiliações não pode ser maior que o número de autores.", font=("Helvetica", 15))
                        else:
            # Atualizar somente as afiliações fornecidas
                            for i, afiliacao in enumerate(lista_afiliacoes):
                                selected_pub["authors"][i]["affiliation"] = afiliacao

                            sg.popup(f"{parametro} atualizado/a com sucesso!", font=("Helvetica", 15))

        parametro_window.close()

    # Salvar o dataset atualizado no arquivo
    fOut = open(fnome, "w", encoding='utf-8')
    json.dump(dataset, fOut, ensure_ascii=False, indent=4)
    fOut.close()

    return dataset

def consultar_publicacao(dataset):

    sg.theme("DarkBlue")

    layout = [
        [sg.Text("Introduza o DOI da publicação que pretende consultar:"), sg.InputText(key="-ID-")],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Sair", key="-SAIR-")],
        [sg.Text("Resultado da consulta:", font=("Helvetica", 12), visible=False, key="-LABEL-")],
        [sg.Multiline(size=(60, 15), key="-RESULTADO-", disabled=True, visible=False)]
    ]

    window1 = sg.Window("Consulta de Publicação", layout, font=("Helvetica", 14), location=(250, 200))

    stop = False
    while not stop:
        event, values = window1.read()
        if event == sg.WINDOW_CLOSED or event == "-SAIR-":
            stop = True
            
        elif event == "-CONSULTAR-":
            doi = values["-ID-"].strip()
            detalhes = None
            res = "Publicação ainda não encontrada"

            # Verificar se o DOI foi fornecido
            if doi:
                for pub in dataset:
                    if pub.get("doi") == doi:
                        detalhes = {
                            "Título": pub.get("title", "Sem título"),
                            "Resumo": pub.get("abstract", "Sem resumo"),
                            "Palavras-chave": pub.get("keywords", "Sem palavras-chave"),
                            "DOI": pub.get("doi", "Sem DOI"),
                            "Link para PDF": pub.get("pdf", "Sem PDF"),
                            "Data de Publicação": pub.get("publish_date", "Sem data"),
                            "URL do Artigo": pub.get("url", "Sem URL"),
                            "Autores": "\n".join(
                                [
                                    f"{autor.get('name', 'Sem nome')} ({autor.get('affiliation', 'Sem afiliação')})"
                                    for autor in pub.get("authors", [{"name": "Sem nome", "affiliation": "Sem afiliação"}])
                                ]
                            ),
                        }
                        res = "\n".join(f"{key}: {value}" for key, value in detalhes.items())

                if detalhes:
                    res_pesquisa["criterios"] = f"Consulta de publicação"
                    res_pesquisa["resultados"] = detalhes
                    window1["-LABEL-"].update(visible=True)
                    window1["-RESULTADO-"].update(res, visible=True)
                else: 
                    sg.popup_error("Não foi encontrada nenhuma publicação com este DOI.")
            else:
                sg.popup_error("Por favor, insira um DOI válido.")

    window1.close()
    return


# Função para consultar publicações por título
def listar_pub_titulo(dataset):
    titulos = sorted([pub.get("title", "Sem título") for pub in dataset if pub.get("title")])

    layout = [
        [sg.Text("Introduza o título da publicação que deseja procurar:")],
        [sg.Text("Título", size=(6, 1)), sg.Combo(titulos, key="-TITULO-", readonly=True)],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Listar por Titulo", layout, size=(1300, 150), location=(200, 300), font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONSULTAR-":
            titulo = values["-TITULO-"]
            linhas = []
            for pub in dataset:
                if titulo == pub.get("title", "Sem título"):
                    autores = pub.get("authors", [])
                    
                    # Se o campo "authors" não existir ou estiver vazio, exibir "Sem autores"
                    if not autores:  # Caso não haja autores
                        autor_nomes = ["Sem Nome"]
                        autor_afiliacoes = ["Sem afiliação"]
                    else:
                        # Se existir, verificar cada autor
                        autor_nomes = [author.get("name", "Sem Nome") for author in autores]
                        autor_afiliacoes = [author.get("affiliation", "Sem afiliação") for author in autores]

                    linha = [
                        pub.get("doi", "Sem DOI"),
                        pub.get("title", "Sem título"),
                        pub.get("publish_date", "Sem data"),
                        pub.get("keywords", "Sem palavras-chave"),  # Assegura que keywords existe
                        ", ".join(autor_nomes),
                        ", ".join(autor_afiliacoes)
                    ]
                    linhas.append(linha)

            col_widths = [10, 30, 15, 15, 20, 15]

            if linhas:
                res_pesquisa["criterios"] = f"Pesquisa por título: {titulo}"
                res_pesquisa["resultados"] = linhas
                layout1 = [
                    [sg.Table(linhas,
                            ['DOI', 'Título', 'Data de Publicação', 'Palavras-Chave', 'Autor(es)', 'Afiliação'],
                            col_widths=col_widths,
                            auto_size_columns=False,
                            justification='center',
                            num_rows=len(linhas))
                    ],
                    [sg.Button("Fechar", key="-FECHAR-")]
                ]
        
                window1 = sg.Window("Tabela", layout1, location=(0, 0), font=("Helvetica", 15))
                stop1 = False
                while not stop1:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
                        stop1 = True
                window1.close()
            else:
                sg.popup("Não existem publicações com o título fornecido.", font=("Helvetica", 15))

    window.close()
    return


# Função para consultar publicações por autor
def listar_pub_autor(dataset):
    autores = []
    for pub in dataset:
        authors = pub.get("authors", [])  # Se 'authors' não existe, retorna lista vazia
        for author in authors:
            name = author.get("name")  # Tenta obter o nome do autor
            if name and name not in autores:  # Adiciona o nome do autor se não estiver na lista
                autores.append(name)

    autores = sorted(autores)

    layout = [
        [sg.Text("Introduza o nome do autor que deseja procurar:")],
        [sg.Text("Autor", size=(6, 1)), sg.Combo(autores, key="-AUTOR-", readonly=True)],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Listar por Autor", layout, size=(900, 150), location=(200, 300), font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONSULTAR-":
            autor = values["-AUTOR-"]
            linhas = []

            for pub in dataset:
                authors = pub.get("authors", [])  # Se 'authors' não existe, retorna lista vazia
                for author in authors:
                    if autor == author.get("name"):  # Verifica se o nome do autor corresponde
                        linha = [
                            pub.get("doi", "Sem DOI"),  # Caso DOI esteja ausente, usa "Sem DOI"
                            pub.get("title", "Sem título"),  # Caso título esteja ausente, usa "Sem título"
                            pub.get("publish_date", "Sem data"),  # Caso data esteja ausente, usa "Sem data"
                            pub.get("keywords", "Sem palavras-chave"),
                            ", ".join([author.get("name", "Sem Nome") for author in pub.get("authors", [])]),  # Nome do autor
                            ", ".join([author.get("affiliation", "Sem afiliação") for author in pub.get("authors", [])])  # Afiliação do autor
                        ]
                        linhas.append(linha)

            col_widths = [10, 30, 15, 15, 20, 15]

            if linhas:
                res_pesquisa["criterios"] = f"Pesquisa por autor: {autor}"
                res_pesquisa["resultados"] = linhas
                layout1 = [
                    [sg.Table(linhas,
                            ['DOI', 'Título', 'Data de Publicação', 'Palavras-Chave', 'Autor(es)', 'Afiliação'],
                            col_widths=col_widths,
                            auto_size_columns=False,
                            justification='center',
                            num_rows=len(linhas))
                    ],
                    [sg.Button("Fechar", key="-FECHAR-")]
                ]
                window1 = sg.Window("Tabela", layout1, location=(0, 0), font=("Helvetica", 15))
                stop = False
                while not stop:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
                        stop = True
                window1.close()

            else:
                sg.popup("Não existem publicações com o autor fornecido.", font=("Helvetica", 15))

    window.close()
    return

# Função para consultar publicações por afiliação
def listar_pub_afiliacao(dataset):
    afiliacoes = []  
    for pub in dataset:
        for author in pub.get("authors", []):  # Se 'authors' não existe, retorna lista vazia
            # A afiliação de cada autor
            afiliacao = author.get("affiliation", "Sem afiliação")
            if afiliacao not in afiliacoes:
                afiliacoes.append(afiliacao)

    afiliacoes = sorted(afiliacoes)

    layout = [
        [sg.Text("Introduza a afiliação que deseja procurar:")],
        [sg.Text("Afiliação", size=(10, 1)), sg.Combo(afiliacoes, key="-AFILIACAO-", readonly=True)],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Listar por Afiliação", layout, size=(900, 150), location=(200, 300), font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONSULTAR-":
            afiliacao = values["-AFILIACAO-"]
            linhas = []

            for pub in dataset:
                for author in pub.get("authors", []):  # Acessa diretamente os autores
                    # Comparação simples para ver se a afiliação do autor corresponde à pesquisa
                    if afiliacao == author.get("affiliation", "Sem afiliação"):
                        # Tratamento de keywords (campo 'keywords' é uma string)
                        keywords = pub.get("keywords", "Sem palavras-chave")
                        palavras_chave = keywords  # Já está em formato de string, sem necessidade de verificação

                        # Criando linha para exibir a publicação
                        linha = [
                            pub.get("doi", "Sem DOI"),
                            pub.get("title", "Sem título"),
                            pub.get("publish_date", "Sem data"),
                            palavras_chave,  # Apenas usa a string diretamente
                            ", ".join([a.get("name", "Sem nome") for a in pub.get("authors", [])]),
                            ", ".join([a.get("affiliation", "Sem afiliação") for a in pub.get("authors", [])])
                        ]
                        linhas.append(linha)

            col_widths = [10, 30, 15, 15, 20, 15]

            if linhas:
                res_pesquisa["criterios"] = f"Pesquisa por afiliação: {afiliacao}"
                res_pesquisa["resultados"] = linhas 
                layout1 = [
                    [sg.Table(values=linhas,
                              headings=['DOI', 'Título', 'Data de Publicação', 'Palavras-Chave', 'Autor(es)', 'Afiliação'],
                              col_widths=col_widths,
                              auto_size_columns=False,
                              justification='center',
                              num_rows=min(len(linhas), 20))],
                    [sg.Button("Fechar", key="-FECHAR-")]
                ] 
                window1 = sg.Window("Tabela de Publicações", layout1, font=("Helvetica", 15))
                stop = False
                while not stop:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
                        stop = True
                window1.close()
            else:
                sg.popup("Não existem publicações com a afiliação fornecida.", font=("Helvetica", 15))

    window.close()
    return

# Função para filtrar publicações por data de publicação
def listar_pub_data(dataset):
    datas_publicacao = sorted(set(pub.get("publish_date", "Sem data") for pub in dataset)) 

    layout = [
        [sg.Text("Escolha a data de publicação que deseja procurar:")],
        [sg.Text("Data de Publicação"), sg.Combo(datas_publicacao, key="-DATA-", readonly=True)],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Listar por Data de Publicação", layout, size=(900, 150), location=(200, 300), font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONSULTAR-":
            data_publicacao = values["-DATA-"]
            linhas = []

            for pub in dataset:
                if pub.get("publish_date", "Sem data") == data_publicacao:
                    keywords = pub.get("keywords", "Sem palavras-chave")
                    palavras_chave = keywords
                    
                    autores = pub.get("authors", [])
                    autores_nomes = []
                    afiliacoes = []
                    
                    # Processa os autores, verificando se há afiliação
                    for author in autores:
                        nome = author.get('name', 'Sem nome')
                        afiliacao = author.get('affiliation', 'Sem afiliação')
                        autores_nomes.append(nome)
                        afiliacoes.append(afiliacao)

                    # Monta a linha com os dados de cada publicação
                    linha = [
                        pub.get("doi", "Sem DOI"),
                        pub.get("title", "Sem título"),
                        pub.get("publish_date", "Sem data"),
                        palavras_chave,
                        ", ".join(autores_nomes),  # Nomes dos autores
                        ", ".join(afiliacoes)  # Afiliações dos autores
                    ]
                    linhas.append(linha)

            col_widths = [10, 30, 15, 15, 20, 15]

            if linhas:
                layout1 = [
                    [sg.Table(
                        values=linhas,
                        headings=['DOI', 'Título', 'Data de Publicação', 'Palavras-Chave', 'Autor(es)', 'Afiliação'],
                        col_widths=col_widths,
                        auto_size_columns=False,
                        justification='center',
                        num_rows=min(len(linhas), 10),
                        key="-TABELA-",
                        enable_events=True
                    )],
                    [sg.Button("Fechar", key="-FECHAR1-")]
                ] 
                window1 = sg.Window("Tabela", layout1, location=(0, 0), font=("Helvetica", 15))
                stop = False
                while not stop:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED or event == "-FECHAR1-":
                        stop = True
                window1.close()

                # Atualiza o dicionário de resultados de pesquisa
                res_pesquisa["criterios"] = f"Pesquisa por data de publicação: {data_publicacao}"
                res_pesquisa["resultados"] = linhas
            else:
                sg.popup("Não existem publicações com a data de publicação fornecida.", font=("Helvetica", 15))

    window.close()
    return


# Função para consultar publicações por palavras-chave
def listar_pub_palavras_chave(dataset):
    palavras_chave = []  # Lista para armazenar palavras-chave únicas
    for pub in dataset:
        keywords = pub.get("keywords", "Sem palavras-chave")  # .get() para evitar erro se a chave não existir
        palavras = [palavra.strip() for palavra in keywords.split(",")]  # Dividir a string em palavras-chave
        
        for palavra in palavras:
            if palavra not in palavras_chave:
                palavras_chave.append(palavra)  # Adiciona a palavra-chave se não estiver na lista
    palavras_chave.sort()


    layout = [
        [sg.Text("Introduza a palavra-chave que deseja procurar:")],
        [sg.Text("Palavra-chave", size=(15, 1)), sg.Combo(palavras_chave, key="-PALAVRA-", readonly=True)],
        [sg.Button("Consultar", key="-CONSULTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Listar por Palavra-chave", layout, size=(900, 150), location=(200, 300), font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONSULTAR-":
            palavra_chave = values["-PALAVRA-"].strip().lower()  # Normaliza para minúsculas e remove espaços extras
            linhas = []

            for pub in dataset:
                keywords = pub.get("keywords", "Sem palavras-chave")
                palavras = [palavra.strip().lower() for palavra in keywords.split(",")]  # Tratamento correto da string

                if palavra_chave in palavras:  # Verifica se a palavra-chave está na lista
                    linha = [
                        pub.get("doi", "Sem DOI"),
                        pub.get("title", "Sem título"),
                        pub.get("publish_date", "Sem data"),
                        ", ".join([palavra.strip() for palavra in keywords.split(",")]),  # Exibe as palavras-chave corretamente
                        ",".join([author.get("name", "Sem nome") for author in pub.get("authors", [])]),
                        ",".join([author.get("affiliation", "Sem afiliação") for author in pub.get("authors", [])])
                    ]
                    linhas.append(linha)

            col_widths = [10, 30, 15, 15, 20, 15]

            if linhas:
                res_pesquisa["criterios"] = f"Pesquisa por palavras-chave: {palavra_chave}"
                res_pesquisa["resultados"] = linhas 
                layout1 = [
                    [sg.Table(values=linhas,
                            headings=['DOI', 'Título', 'Data de Publicação', 'Palavras-Chave', 'Autor(es)', 'Afiliação'],
                            col_widths=col_widths,
                            auto_size_columns=False,
                            justification='center',
                            num_rows=min(len(linhas), 20))],
                    [sg.Button("Fechar", key="-FECHAR-")]
                ] 
                window1 = sg.Window("Tabela", layout1, location=(0, 0), font=("Helvetica", 15))  
                stop = False
                while not stop:
                    event, values = window1.read()
                    if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
                        stop = True
                window1.close()
            else:
                sg.popup("Não existem publicações com a palavra-chave fornecida.", font=("Helvetica", 15))

    window.close()
    return

# função para eliminar publicações
def eliminarPub(dataset, fnome):
    with open(fnome, "r", encoding="utf-8") as fIn:
        publicacoes = json.load(fIn)

    # Layout inicial para inserção do DOI
    doi_layout = [
        [sg.Text("Insira o DOI da publicação que deseja remover:")],
        [sg.InputText(key="-DOI-", size=(50, 1))],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    doi_window = sg.Window("Remover Publicação por DOI", doi_layout, font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = doi_window.read()

        if event in (sg.WINDOW_CLOSED, "-CANCELAR-"):
            stop = True  # Fecha a janela se o evento for cancelar ou fechamento
            doi_window.close()
            return dataset  # Retorna o dataset sem alterações

        if event == "-CONFIRMAR-":
            doi_input = values["-DOI-"].strip()  # Obtém o DOI inserido pelo usuário

            if not doi_input:
                sg.popup("Por favor, insira um DOI válido.", font=("Helvetica", 15))
            else:
                # Verifica se o DOI existe no dataset
                publicacao_encontrada = None
                for i, pub in enumerate(dataset):
                    if pub.get("doi") == doi_input:
                        publicacao_encontrada = i  # Salva o índice da publicação encontrada

                if publicacao_encontrada is not None:
                    # Confirmação de remoção
                    resposta = sg.popup_yes_no(
                        f"Tem a certeza que deseja remover a publicação com DOI: {doi_input}?",
                        font=("Helvetica", 15)
                    )
                    if resposta == "Yes":
                        dataset.pop(publicacao_encontrada)  # Remove a publicação
                        sg.popup(f"Publicação com DOI: {doi_input} foi removida com sucesso.", font=("Helvetica", 15))
                        stop = True  # Sai do loop após remoção
                else:
                    sg.popup("DOI não encontrado no dataset. Tente novamente.", font=("Helvetica", 15))

    # Salvar o dataset atualizado no arquivo
    fOut = open(fnome, "w", encoding='utf-8')
    json.dump(dataset, fOut, ensure_ascii=False, indent=4)
    fOut.close()

    doi_window.close()
    return dataset


# função para listar autores e publicações associadas
def listar_autores_e_publicacoes(dataset):
    
    autores_dict = {}   # Dicionário para armazenar o número de publicações por autor

    for publicacao in dataset:  # Percorrer todas as publicações   
        autores = [author.get('name', 'Autor desconhecido').strip() for author in publicacao.get('authors', [])]
        
        for autor in autores:   # Adicionar cada autor ao dicionário e contar as publicações
            autor = autor.strip()  # Remover espaços extras ao redor do nome do autor
            if autor in autores_dict:
                autores_dict[autor] += 1  # Incrementar a contagem de publicações
            else:
                autores_dict[autor] = 1  # Se o autor ainda não está no dicionário, inicializa com 1

    # Perguntar ao usuário qual critério de ordenação ele prefere
    ord_layout = [
        [sg.Text("Escolha como deseja ordenar os autores:")],
        [sg.Radio("Por frequência de publicações", "ORDENACAO", key="-FREQUENCIA-", default=True)],
        [sg.Radio("Por ordem alfabética", "ORDENACAO", key="-ALFABETICA-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    ord_window = sg.Window("Escolher Ordem de Autores", ord_layout, font=("Helvetica", 15))

    stop = False
    autores_ordenados = []
    while not stop:
        event, values = ord_window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
            ord_window.close()
        elif event == "-CONFIRMAR-":
            # Ordenar de acordo com a escolha do usuário
            if values["-FREQUENCIA-"]:
                # Ordenar por frequência (decrescente)
                autores_ordenados = sorted(autores_dict.items(), key=lambda x: (-x[1], x[0]))
            elif values["-ALFABETICA-"]:
                # Ordenar por nome do autor (alfabeticamente)
                autores_ordenados = sorted(autores_dict.items(), key=lambda x: x[0])
            stop = True


    progress_layout = [
        [sg.Text("Processando...")],
        [sg.ProgressBar(len(autores_ordenados), orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    progress_window = sg.Window("Processamento", progress_layout,size=(300, 100), finalize=True)


    if autores_ordenados:
        
        res = []   # lista de resultados
        for index, (autor, quantidade) in enumerate(autores_ordenados):
            publicacoes_autor = []
            for publicacao in dataset:
                for author in publicacao.get('authors', []):
                    if autor.lower() == author.get('name', '').lower():  # Verifica se o autor é o mesmo
                        titulo = publicacao.get('title', 'Título não disponível')
                        publish_date = publicacao.get('publish_date', 'Data não disponível')
                        publicacoes_autor.append(f"{titulo} ({publish_date})")
            res.append([autor, quantidade, ', '.join(publicacoes_autor)])

            # Atualiza a barra de progresso durante o processamento
            event, values = progress_window.read(timeout=0)
            if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
                progress_window.close()
                return  # Se o usuário cancelar, sai da função
            progress_window['-PROGRESS-'].update_bar(index + 1)
        
        progress_window.close()
        ord_window.close()

        # mostrar resultados numa tabela
        col_widths = [20, 20, 30]
            
        res_layout = [
            [sg.Table(values=res, headings=["Autor", "Nº Publicações", "Publicações"], auto_size_columns=False, col_widths = col_widths  , justification="center", key="-TABELA-", enable_events=True)],
            [sg.Button("Fechar", key="-FECHAR-")]
        ]
            
        res_window = sg.Window("Análise de Autores e Publicações", res_layout, font=("Helvetica", 15))
            
        stop1 = False
        while not stop1:
            event, values = res_window.read()
            if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
                stop1 = True
        res_window.close()  
        res_pesquisa["criterios"] = "Pesquisa por autores e publicações associadas"
        res_pesquisa["resultados"] = res



# função para listar palavras-chave e publicações associadas
def analise_por_palavras_chave(dataset):

    palavras_chave_dict = {}    # Dicionário para armazenar a quantidade de ocorrências de cada palavra-chave

    for publicacao in dataset:
        keywords = publicacao.get('keywords', '')

        palavras_chave = keywords.split(',')  # Separa por vírgulas
    
        palavras_chave = [p.strip().lower() for p in palavras_chave if p.strip()] # Remover espaços e converte para minúsculas
               
        for palavra in palavras_chave:  # Contagem das ocorrências de cada palavra-chave
            palavra = palavra.strip().lower()
            if palavra in palavras_chave_dict:
                palavras_chave_dict[palavra] += 1
            else:
                palavras_chave_dict[palavra] = 1

    ord_layout = [      # escolher o critério de ordenação
        [sg.Text("Escolha como deseja ordenar as palavras-chave:")],
        [sg.Radio("Por frequência de ocorrências", "ORDENACAO", key="-FREQUENCIA-", default=True)],
        [sg.Radio("Por ordem alfabética", "ORDENACAO", key="-ALFABETICA-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    ord_window = sg.Window("Escolher Ordem das Palavras-Chave", ord_layout, font=("Helvetica", 15))
    
    stop = False
    while not stop:
        event, values = ord_window.read()
        
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
            ord_window.close()
        elif event == "-CONFIRMAR-":
            if values["-FREQUENCIA-"]:
                palavras_chave_ordenadas = sorted(palavras_chave_dict.items(), key=lambda x: (-x[1], x[0]))
            elif values["-ALFABETICA-"]:
                palavras_chave_ordenadas = sorted(palavras_chave_dict.items(), key=lambda x: x[0])
            
            stop = True
            ord_window.close()

    # janela de progresso é aberta após o clique no "Confirmar"
    progress_layout = [
        [sg.Text("Processando...")],
        [sg.ProgressBar(len(palavras_chave_ordenadas), orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    progress_window = sg.Window("Processamento", progress_layout,size=(300, 100), finalize=True)

    # Processar as palavras-chave e publicações associadas com barra de progresso
    res = []
    for index, (palavra, quantidade) in enumerate(palavras_chave_ordenadas):
        publicacoes_palavra = []
        for publicacao in dataset:
            pub_keywords = publicacao.get('keywords', '').split(',')  # Obter as palavras-chave
            if palavra.lower() in [k.strip().lower() for k in pub_keywords]:
                 # Usar .get() para evitar KeyError caso a chave não exista
                title = publicacao.get('title', 'Título não disponível')
                publish_date = publicacao.get('publish_date', 'Data não disponível')
                publicacoes_palavra.append(f"{title} ({publish_date})")
        
        res.append([palavra, quantidade, ', '.join(publicacoes_palavra)])

        event, values = progress_window.read(timeout=0)
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            progress_window.close()
            return  # Se cancelar, sai da função
        progress_window['-PROGRESS-'].update_bar(index + 1)     # atualização da barra de progresso

    progress_window.close()

    col_widths = [20, 10, 30]
    res_layout = [
        [sg.Table(values=res, headings=["Palavra-chave", "Ocorrências", "Publicações"], col_widths=col_widths,
                  auto_size_columns=False, justification="center", key="-TABELA-", enable_events=True)],
        [sg.Button("Fechar", key="-FECHAR-")]
    ]
    res_window = sg.Window("Análise de Palavras-chave e Publicações", res_layout, font=("Helvetica", 15))
    
    stop1 = False
    while not stop1:
        event, values = res_window.read()
        if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
            stop1 = True
    
    res_window.close()


# função para importar dados/ publicações
def importarPublicacoes(dataset, fnome):
    layout = [
        [sg.Text("Selecione o arquivo JSON para importar publicações:")],
        [sg.InputText(key="-ARQUIVO-", readonly=True, size=(50, 1)), sg.FileBrowse(file_types=(("Arquivos JSON", "*.json"),))],
        [sg.Button("Importar", key="-IMPORTAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Importar Publicações", layout, font=("Helvetica", 15))

    stop = False
    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
            window.close()
            return dataset  # Retorna o dataset sem alterações, caso o usuário cancele

        if event == "-IMPORTAR-":
            arquivo = values["-ARQUIVO-"]  # Obter o caminho do arquivo JSON selecionado
            if arquivo:  # Verificar se o usuário selecionou um arquivo
                try:
                    with open(arquivo, "r", encoding="utf-8") as file:
                        novas_publicacoes = json.load(file)

                    # Variável para contar quantas publicações novas foram adicionadas
                    novas_adicionadas = 0

                    # Criar um conjunto de DOIs já existentes no dataset
                    doois_existentes = {pub["doi"] for pub in dataset if "doi" in pub}

                    # Adicionar as publicações novas ao dataset
                    for pub in novas_publicacoes:
                        if "doi" in pub and pub["doi"] not in doois_existentes:
                            dataset.append(pub)
                            novas_adicionadas += 1
                            doois_existentes.add(pub["doi"])  # Adiciona o DOI ao conjunto

                            with open(fnome, "w", encoding="utf-8") as fOut:
                                json.dump(dataset, fOut, ensure_ascii=False, indent=4)
                            sg.popup("Dataset atualizado com sucesso!")
                            return dataset
        
                    if novas_adicionadas > 0:
                        sg.popup(f"{novas_adicionadas} novas publicações foram importadas com sucesso!")
                    else:
                        sg.popup("Não foram encontradas publicações novas para importar.")

                except Exception as e:
                    sg.popup_error(f"Ocorreu um erro ao importar o arquivo: {e}")

            else:
                sg.popup_error("Por favor, selecione um arquivo JSON.")

        window.close()
        return dataset

    # Salvar o dataset atualizado no arquivo (aqui é o momento de 'escrever')
    try:
        with open(fnome, "w", encoding="utf-8") as fOut:
            json.dump(dataset, fOut, ensure_ascii=False, indent=4)
        sg.popup("Dataset atualizado com sucesso!")
    except Exception as e:
        sg.popup_error(f"Ocorreu um erro ao salvar o arquivo: {e}")

    return dataset


def exportarPesquisa():
    
    try:
        # verificar se a variável res_pesquisa tem dados (resultado da pesquisa)
        if not res_pesquisa:
            sg.popup("Nenhum dado para exportar. Realize uma pesquisa primeiro.", title="Erro", font=("Helvetica", 12))
            return
        
        # permite ao usuário escolher o nome e a localização do arquivo
        filepath = sg.popup_get_file("Escolha onde deseja salvar o arquivo", save_as=True, file_types=(("JSON Files", "*.json"),))
        
        if not filepath:    # verifica se o usuário cancelou a escolha
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:        # guarda os resultados da pesquisa no arquivo JSON
            json.dump(res_pesquisa, f, ensure_ascii=False, indent=4)
        sg.popup(f"Última pesquisa exportada com sucesso para '{filepath}'!", title="Exportação Concluída", font=("Helvetica", 12))
    
    except Exception as e:
        sg.popup(f"Erro ao exportar a pesquisa: {e}", title="Erro", font=("Helvetica", 12))