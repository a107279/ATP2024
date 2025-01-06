import FreeSimpleGUI as sg
import Graficos
import AppPub


sg.theme("LightBrown10")

layout = [
    [sg.Text("Consulta e Análise de Publicações Científicas ", font=("Helvetica", 15), justification="center")],
    [sg.Button("Iniciar", size=(20,2),key="-INICIAR-"), sg.Button("Sair",size=(20,2), key="-SAIR-")]
]

window = sg.Window("Consulta e Análise de Publicações Científicas", layout, size=(435, 90), finalize=True)

stop=False
while not stop:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "-SAIR-":
        stop=True
    elif event == "-INICIAR-":
        window.close()

        # menu principal
        carregou_base = False  # Variável para verificar se a base foi carregada
        lista_menu = [
            [sg.Text("Menu Principal", font=("Arial", 20), justification="center", expand_x=True)],
            [sg.Button("Carregar Base de Dados", key="-CARREGAR-")],
            [sg.Button("Help", key="-HELP-", disabled=True)],
            [sg.Button("Criar Publicação", key="-CRIARPUB-", disabled=True)],
            [sg.Button("Consulta de Publicação", key="-CONSULTADEPUB-", disabled=True)],
            [sg.Text("Consulta de Publicação Por:", key="-CONSULTA-"), 
             sg.Radio("Título", key="-CT-", group_id="consulta", disabled=True), sg.Radio("Data de publicação", key="-CD-", group_id="consulta", disabled=True), 
             sg.Radio("Afiliação", key="-CA-", group_id="consulta", disabled=True),sg.Radio("Autor", key="-CAU-", group_id="consulta", disabled=True), 
             sg.Radio("Palavra-Chave", key="-CP-", group_id="consulta", disabled=True), sg.Button("Consultar", key="-CONSULTAR-", disabled=True)],
            [sg.Button("Atualizar Publicação", key="-ATUALIZARPUB-",  disabled=True)],
            [sg.Button("Eliminar Publicação", key="-ELIMINARPUB-", disabled=True)],
            [sg.Button("Relatório de Estatísticas", key="-GERARREL-", disabled=True)],
            [sg.Button("Listar Autores", key="-LISTARAUTH-", disabled=True)],
            [sg.Button("Listar Palavras-Chave", key="-LISTARPC-", disabled=True)],
            [sg.Button("Importar Publicações", key="-IMPORTARPUB-", disabled=True)],
            [sg.Button("Guardar Publicações", key="-GUARDARPUB-", disabled=True)],
            [sg.Button("Exportar Última Pesquisa", key="-EXPORTAR-", disabled= True)],
            [sg.Button("Sair", key="-SAIR-")]
        ]

        window = sg.Window("Menu Principal", lista_menu, font=('Arial'), finalize=True)

        carregou_bd= False
        stop = False
        while not stop:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "-SAIR-":
                stop=True
            elif event == "-CARREGAR-": 
                file = AppPub.procuraFicheiro()
                if not file:
                    sg.popup("Ficheiro não selecionado", title="Erro", font=("Helvetica", 12), text_color="red")
                else:
                    publicacoes = AppPub.carregaDados(file)
        
                    if not publicacoes:  # Se o retorno for uma lista vazia (indicando erro no JSON)
                        sg.popup("Erro ao carregar o arquivo. O conteúdo não é válido JSON.", title="Erro", font=("Helvetica", 12), text_color="red")
                        carregou_bd = False  # Impede que a base de dados seja considerada carregada
                    else:
                        sg.popup(f"Foram carregados {len(publicacoes)} publicações.", title="Base de Dados Carregada", font=("Helvetica", 12))
                        carregou_bd = True

                        window['-HELP-'].update(disabled=False)
                        window['-CRIARPUB-'].update(disabled=False)
                        window['-CONSULTADEPUB-'].update(disabled=False)
                        window['-ATUALIZARPUB-'].update(disabled=False)
                        window['-ELIMINARPUB-'].update(disabled=False)
                        window['-CONSULTAR-'].update(disabled=False)
                        window['-CT-'].update(disabled=False)
                        window['-CP-'].update(disabled=False)
                        window['-CA-'].update(disabled=False)
                        window['-CAU-'].update(disabled=False)
                        window['-CD-'].update(disabled=False)
                        window['-GERARREL-'].update(disabled=False)
                        window['-LISTARAUTH-'].update(disabled=False)
                        window['-LISTARPC-'].update(disabled=False)
                        window['-IMPORTARPUB-'].update(disabled=False)
                        window['-EXPORTAR-'].update(disabled=False)
                        window['-GUARDARPUB-'].update(disabled=False)
            
            elif event == "-HELP-":
                AppPub.print_help()
            
            elif event == "-CRIARPUB-":
                if carregou_bd:
                    AppPub.criar_publicacao(publicacoes, file)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
            
            elif event == "-CONSULTADEPUB-":
                if carregou_bd:
                    res_pesquisa = AppPub.consultar_publicacao(publicacoes)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
            
            elif event == "-ATUALIZARPUB-":
                if carregou_bd:
                    AppPub.atualizar_publicacao(publicacoes, file)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))

            elif event == "-ELIMINARPUB-":
                if carregou_bd:
                    AppPub.eliminarPub(publicacoes, file)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))

            elif event == "-LISTARAUTH-":
                if carregou_bd:
                    AppPub.listar_autores_e_publicacoes(publicacoes)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
            
            elif event =="-LISTARPC-":
                if carregou_bd:
                    AppPub.analise_por_palavras_chave(publicacoes)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))

            elif event == "-CONSULTAR-":
                if values["-CT-"]:
                    sg.popup("Consultando por Título", title="Consulta")
                    if carregou_bd:
                        AppPub.listar_pub_titulo(publicacoes)
                    else:
                        sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
                elif values["-CAU-"]:
                    sg.popup("Consultando por Autor", title="Consulta")
                    if carregou_bd:
                        AppPub.listar_pub_autor(publicacoes)
                    else:
                        sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
                elif values["-CA-"]:
                    sg.popup("Consultando por Afiliação", title="Consulta")
                    if carregou_bd:
                        AppPub.listar_pub_afiliacao(publicacoes)
                    else:
                        sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
                elif values["-CD-"]:
                    sg.popup("Consultando por Data de Publicação", title="Consulta")
                    if carregou_bd:
                        AppPub.listar_pub_data(publicacoes)
                    else:
                        sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
                elif values["-CP-"]:
                    sg.popup("Consultando por Palavra-Chave", title="Consulta")
                    if carregou_bd:
                        AppPub.listar_pub_palavras_chave(publicacoes)
                    else:
                        sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))

            elif event == "-EXPORTAR-":
                if carregou_bd:
                    AppPub.exportarPesquisa()  
                else:
                    sg.popup("Primeiro, faça uma pesquisa para guardar os resultados.", title="Erro", font=("Helvetica", 12))
            
            elif event == "-GERARREL-":
                if carregou_bd:
                    Graficos.exibir_menu_relatorios(publicacoes)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
    
            elif event == "-IMPORTARPUB-":
                if carregou_bd:
                    AppPub.importarPublicacoes(publicacoes, file)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))

            elif event == "-GUARDARPUB-":
                if carregou_bd:
                    AppPub.salvaDados(publicacoes)
                else:
                    sg.popup("Primeiro, carregue a base de dados.", title="Erro", font=("Helvetica", 12))
            
            else: 
                stop = True
        
        window.close()
             


            
       
